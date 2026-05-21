# INGESTION 

## Architecture Decisions

### Why Function App over a VM
- Serverless PaaS - no need to manage or pay when idle
- Consumption plan allows for pay-as-you-go
- Auto scaled 

### Why Managed Identity over storage account keys or service principal
- Fully managed by Azure - no need for expiring secret keys or managing a client id 
- Credentials not stored in code/variables. MI completely eliminates a potential leak
- Authentication is handled by Azure AD - installed azure.identity and used the corresponding class (DefaultAzureCredential) for auto authentication based on az login session 

### Why the timer trigger
- Data needs to retrieved on a schedule, not on demand 
- Cron expression was used - fires at midnight and 12pm UTC daily for pre and post game data capture

### Why host.json and requirement.txt
- **host.json** — minimum config file Azure Functions requires at the project root to identify it as a Function App project
- **requirements.txt** — tells Azure which Python packages to install when deploying. Without it, Azure has no libraries and the function crashes immediately
- **function.json** — tells Azure the trigger type and schedule for that specific function. Azure reads it automatically from the same folder as `__init__.py`

## Development Approach
- Developed and tested locally first by retrieving API data and dumping into a local file using 'if __name__ == "__main__"' before deploying to Azure
- Timer trigger was tested temporarily by setting cron expression to every 2 minutes
- Caught a filesystem error - AZ Function Apps cannot use local disks to write data to. Local file writes were removed to support streaming of API responses directly to the blob 
- Iterative deploy cycle - fix error locally → redeploy → check Monitor invocation logs in portal