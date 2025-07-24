# Sendgrid Cronjob - MCP
[![smithery badge](https://smithery.ai/badge/@chaser164/sendgrid-cronjob-mcp)](https://smithery.ai/server/@chaser164/sendgrid-cronjob-mcp)

## Description
This integration provides an MCP server that allows Claude to retrieve and execute cron jobs that schedule email sends via SendGrid.

## Prerequisites
- Claude Desktop installed on your local machine.
- Node.js (version 14 or higher) installed.

## Configuration
Before starting the Sendgrid Cronjob - MCP, user-specific configurations are required:
1. Add the following Environment Variables:
   - `SENDGRID_API_KEY`: Your `sendgrid.com` API key
   - `CRONJOB_API_KEY`: Your `cron-job.org` API key
   - `FROM_EMAIL`: Email address of an authenticated SendGrid single sender identity
   - `TZ`: Your system's timezone (optional, default is UTC). Choose timezone string from [this list](https://www.w3schools.com/php/php_ref_timezones.asp).

   
## Installation

### Installing via Smithery

To install sendgrid-cronjob-mcp for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@chaser164/sendgrid-cronjob-mcp):

```bash
npx -y @smithery/cli install @chaser164/sendgrid-cronjob-mcp --client claude
```

### Installing Manually
#### 1. Clone Repository
- Open your terminal or command line.
- Run `git clone https://github.com/chaser164/sendgrid-cronjob-mcp.git`

```
{
  "mcpServers": {
    "cronjob_email_mcp": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/sendgrid-cronjob-mcp",
        "run",
        "email-schedule-send-mcp-server.py"
      ],
      "env": {
        "SENDGRID_API_KEY": "<SendGrid API key>",
        "CRONJOB_API_KEY": "<Cron Job API key>",
        "FROM_EMAIL": "<SendGrid sender identity email>"
        "TZ": "<timezone value>",
      }
      
    }
  }
}
```

## Usage

- Ask your LLM to create, get, and delete scheduled emails
- If a "to email" is not specified, the mcp will send an email to yourself (e.g., "remind me to dance" will send an email to yourself)

## License
This project is licensed under the MIT License.

## Contributions
Contributions are welcome. Feel free to open issues or submit a pull request for feature enhancements or bug fixes.
