# CronGrid — an MCP server scheduling SendGrid Cron Jobs!
[![smithery badge](https://smithery.ai/badge/@chaser164/crongrid-mcp)](https://smithery.ai/server/@chaser164/crongrid-mcp)

## Description
This MCP server enables LLMs to POST, GET, and DELETE cron jobs that schedule email sends via SendGrid.


## Prerequisites
- Claude Desktop (or another MCP server-compatible LLM interface of your choice) installed on your local machine.
- If using Smithery: [Node.js](https://nodejs.org/en/download) (version 14 or higher) installed
- If running locally: [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.
- 

## Installation

### Installing via Smithery

To install CronGrid automatically via [Smithery](https://smithery.ai/server/@chaser164/crongrid-mcp) (example for Claude Desktop):

```bash
npx -y @smithery/cli install @chaser164/sendgrid-cronjob-mcp --client claude
```

### Installing Manually

- Open your terminal or command line.
- Run `git clone https://github.com/chaser164/sendgrid-cronjob-mcp.git`
- Add the below to your MCP server-compatible interface of choice (e.g., `~/Library/Application Support/Claude/claude_desktop_config.json`)

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

**NOTE**: timezone environment variable values must be chosen from [this list](https://www.w3schools.com/php/php_ref_timezones.asp). The default timezone value is `UTC`.

## Usage

- Ask your LLM to create, get, and delete scheduled emails
- This MCP also has the ability to get the current date/time to enhance its scheduling capabilities
- If a "to email" is not specified, the mcp will send an email to yourself (e.g., "remind me to dance" will send an email to the specified SendGrid sender identity's email address)

## License
This project is licensed under the MIT License.

## Contributions
Contributions are welcome. Feel free to open issues or submit a pull request for feature enhancements or bug fixes.
