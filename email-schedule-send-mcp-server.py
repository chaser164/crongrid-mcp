from typing import Any
import httpx
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from mcp.server.fastmcp import FastMCP
from datetime import timedelta
import pytz

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Environment variables from .env file will not be loaded.")

USING_BACKUP_TZ = False

# global constants
TZ = os.getenv("TZ", "UTC")
if TZ not in pytz.all_timezones:
    print(f"Warning: Invalid timezone: {TZ}. Using UTC. please change the TZ environment variable to a valid timezone")
    USING_BACKUP_TZ = True
    TZ = "UTC"

CRONJOB_API_BASE = "https://api.cron-job.org"

# Initialize FastMCP server
mcp = FastMCP("Email Schedule Send")

# make_cronjob_request makes API calls to the cron-job.org API
async def make_cronjob_request(method: str, url: str, json_data: dict = None) -> dict[str, Any] | None:
    """Make a request to the cron-job.org API with proper error handling."""
    api_key = os.getenv("CRONJOB_API_KEY")
    if not api_key:
        raise ValueError("CRONJOB_API_KEY environment variable is required")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers, timeout=30.0)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=json_data, timeout=30.0)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

@mcp.tool()
async def delete_scheduled_email(job_id: str) -> str:
    """Delete a specific scheduled email cron job by ID.

    Args:
        job_id: The ID of the cron job to delete
    """
    url = f"{CRONJOB_API_BASE}/jobs/{job_id}"
    result = await make_cronjob_request("DELETE", url)
    
    if "error" not in result:
        return f"Successfully deleted cron job {job_id}"
    else:
        return f"Failed to delete cron job {job_id}"

@mcp.tool()
async def get_scheduled_emails() -> str:
    """Get all scheduled email cron jobs for the account."""
    url = f"{CRONJOB_API_BASE}/jobs"
    result = await make_cronjob_request("GET", url)
    
    if result and "error" not in result:
        if "jobs" in result and result["jobs"]:
            jobs_info = []
            for job in result["jobs"]:
                job_info = f"""
Job ID: {job.get('jobId', 'Unknown')}
Title: {job.get('title', 'Unknown')}
URL: {job.get('url', 'Unknown')}
Enabled: {job.get('enabled', 'Unknown')}
Schedule: {job.get('schedule', 'Unknown')}
"""
                jobs_info.append(job_info)
            return "\n---\n".join(jobs_info)
        else:
            return "No cron email jobs found"
    elif result and "error" in result:
        return f"Error fetching email cron jobs: {result['error']}"
    else:
        return "Failed to fetch email cron jobs"

@mcp.tool()
async def create_scheduled_email_send_at_specific_time(
    title: str,
    subject: str,
    body: str,
    minutes: list[int],
    hours: list[int],
    mdays: list[int],
    months: list[int],
    wdays: list[int],
    timezone: str = TZ,
    expires_at: int = 0, # 0 = never expires
    to_email: str = None,
    repeating: bool = False
) -> str:
    """This tool creates a new scheduled email cron job at a specified date(s)/time(s) in cronjob format, setting up a cron-job that calls an email-sending API. The scheduled email can either be a one-time email or a recurring email.
    Never make a scheduled email cron job repeating (the final argument of the function) unless the user explicitly asks for it; assume the user wants a one-time email unless they explicitly ask for a repeating email send.
    If the user does not provide a to_email parameter, the email will be sent to the FROM_EMAIL environment variable (email to self). 
    So, do not provide a to_email parameter when the user requests an email to self (e.g. "send an email to myself," "remind me to do something," "create a reminder," "send me an email," etc.). 
    Expiration is automatically set for one-time emails. For repeating emails, expiration is up to the user; it is defaulted to 0, which means the email will be sent indefinitely. Assume the user does not want the repeated send to expire unless they explicitly ask for it.
    Repeated emails have a [-1] as one of the time parameters, which means the email will be sent every minute, hour, day, month, or week. Non-repeated emails only have non-negative time parameters.
    If the user asks for an email at a relative time, you can use the get_current_datetime tool to get the current time in the user's timezone and then use that to schedule the email. ALWAYS use the default timezone value unless the user explicitly asks for a different timezone.
    

    Args:
        title: Title for the email cron job
        subject: Email subject
        body: Email body content
        minutes: Minutes to run (0-59, or [-1] for every minute).
        hours: Hours to run (0-23, or [-1] for every hour).
        mdays: Days of month to run (1-31, or [-1] for every day).
        months: Months to run (1-12, or [-1] for every month). 
        wdays: Days of week to run (0-6 where 0=Sunday, or [-1] for every day).
        expires_at: Date/time (in job’s time zone) after which the job expires, i.e. after which it is not scheduled anymore (format: YYYYMMDDhhmmss, 0 = does not expire)
        to_email: Recipient email address. Default is None, which means the email will be sent to the FROM_EMAIL environment variable (email to self).
        repeating: Whether the email should be sent repeatedly. Default is False, which means the email will be sent only once.
    """

    # ensure non-repeating is set appropriately
    if not repeating:
        for m in minutes:
            assert m != -1, "Minutes cannot be -1 for a one-time email, try again"
        for h in hours:
            assert h != -1, "Hours cannot be -1 for a one-time email, try again"
        for d in mdays:
            assert d != -1, "Days of month cannot be -1 for a one-time email, try again"
        for m in months:
            assert m != -1, "Months cannot be -1 for a one-time email, try again"

        # ensure expiration after one call for non-repeating emails
        expires_at = int((datetime.now() + timedelta(days=365)).strftime("%Y0101000000"))
    elif expires_at != 0:
        # for repeating jobs, ensure expiration is in the future if it exists
        assert expires_at > int(datetime.now().strftime("%Y%m%d%H%M%S")), "Expiration time must be in the future, try again"

    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    if not sendgrid_api_key:
        return "Error: SENDGRID_API_KEY environment variable is required"

    from_email = os.getenv("FROM_EMAIL")
    if not from_email:
        return "Error: FROM_EMAIL environment variable is required"
    
    url = f"{CRONJOB_API_BASE}/jobs"

    # set to_email to from_email if not provided (email to self)
    if to_email is None:
        to_email = from_email
    
    job_data = {
        "job": {
            "url": "https://api.sendgrid.com/v3/mail/send",
            "title": title,
            "enabled": True,
            "schedule": {
                "timezone": timezone,
                "expiresAt": expires_at,
                "hours": hours,
                "mdays": mdays,
                "minutes": minutes,
                "months": months,
                "wdays": wdays
            },
            "requestMethod": 1,
            "extendedData": {
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {sendgrid_api_key}"
                },
                "body": f'{{"personalizations": [{{"to": [{{"email": "{to_email}"}}]}}],"from": {{"email": "{from_email}"}},"subject": "{subject}","content": [{{"type": "text/plain", "value": "{body}"}}]}}'
            }
        }
    }
    
    result = await make_cronjob_request("PUT", url, job_data)
    
    if result and "error" not in result:
        job_id = result.get("jobId", "Unknown")
        return f"Successfully scheduled email cron job '{title}' with ID: {job_id}"
    elif result and "error" in result:
        return f"Error scheduling email cron job: {result['error']}"
    else:
        return "Failed to schedule email cron job"


@mcp.tool()
async def get_current_datetime() -> str:
    """Get the current date and time in the system's local timezone or TZ environment variable. This function will give you the full context to schedule a cron job.
    For example, if asked to schedule an email an hour from now, you can look at the output of this function to understand when that would be in the future. 
    This is also useful in case the user wants to know the current time for any reason, or if you require the current time for any reason.

    
    Returns:
        Formatted datetime string with timezone information
    """
    
    try:
        # Use the timezone returned by helper function
        tz = ZoneInfo(TZ)
        current_time = datetime.now(tz)
        ret_string = f"Current time in {TZ}: {current_time.strftime('%A, %Y-%m-%d %H:%M:%S %Z')}"
        if USING_BACKUP_TZ:
            ret_string += f"\n\Please warn user of invalid timezone: {TZ}. Using UTC as fallback. please change the TZ environment variable to a valid timezone"
        return ret_string
    except Exception as e:
        return f"Error: Unable to get current time: {str(e)}"


if __name__ == "__main__":
    # Initialize and run the server
    print(f"Email scheduler server starting...")
    mcp.run(transport='stdio')
    