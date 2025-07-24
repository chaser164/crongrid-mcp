# Sendgrid Cronjob - MCP
[![smithery badge](https://smithery.ai/badge/@chaser164/sendgrid-cronjob-mcp)](https://smithery.ai/server/@chaser164/sendgrid-cronjob-mcp)

## Description
This integration provides an MCP server that allows Claude to retrieve and execute cron jobs from the SendGrid API on a user-specified interval.

## Prerequisites
- Claude Desktop installed on your local machine.
- Node.js (version 14 or higher) installed.

## Configuration
Before starting the Sendgrid Cronjob - MCP, user-specific configurations are required:
1. Add the following Environment Variables:
   - `SENDGRID_API_KEY`: Your SendGrid API key.
   - `CRON_INTERVAL`: The desired interval for cron jobs in cron format.
   
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

#### 2. Install Dependencies
In the root directory of the cloned repository, run `npm install` to install the necessary dependencies.

#### 3. Run the Server
After installing dependencies, run `node index.js` to start the MCP server.

## Usage
- Follow the configuration guide described above.
- Launch Claude and use the MCP client to connect to the Sendgrid Cronjob - MCP server.
- Define a prompt to interact with the cron jobs retrieved from SendGrid.

## Troubleshooting
- Ensure environment variables are set correctly.
- Verify if `node` and `npm` are installed and available in the system PATH.
- Check connectivity between Claude and the MCP server.

## License
This project is licensed under the MIT License.

## Contributions
Contributions are welcome. Feel free to open issues or submit a pull request for feature enhancements or bug fixes.
