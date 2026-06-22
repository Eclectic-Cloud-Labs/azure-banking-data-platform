# Serve Azure SQL & Data Factory - PHASE 4

## Whats been built 
- Azure SQL Server and Basic tier database as the serving layer for gold data
- Azure Data Factory pipeline to move gold Delta tables from ADLS Gen2 into Azure SQL
- Two tables created - WL (season win/loss record) and GOALDIFF (goal differential by opponent)
- Schedule for pipeline runs every 12 hours, 30 minutes after the original pipeline ingests and transforms the data, allowing for sufficient time for data transformation and cluster starting (for dev environment)


## Architecture Decisions

### Why Azure SQL over reading Delta directly
- Universal accessibility. Any tool, application, or analyst can connect via standard SQL connection string
- No Spark or Databricks knowledge required for consumers
- Matches how banks expose structured data to teams and dashboards

### Why Data Factory over a Python script
- Has orchestration, retry logic, monitoring, and logging. No fiddling with custom errors - PaaS easier to deal with
- I wanted to mimic a production grade pattern used in enterprise Azure environments

### Why canadacentral for SQL Server
- East US region was not accepting new SQL Server creation at time of deployment
- In production all services would be in the same region to avoid cross region egress costs and latency

## Issues & Resolutions
- MFA authentication not supported in VS Code SQL extension so i switched to SQL admin credentials
- Local machine IP and data factory integration runtime was not whitelisted on SQL Server firewall. Had to add firewall rule for local IP
- "WL" table had no natural key for upsert. Issue resolved using TRUNCATE TABLE pre-copy script with insert write behaviour instead of Upsert
- "WL" was not triggering successfully. After inspecting the code and error, testing all connections from datasets, resetting the linked services, I realized it was case sensitive - changed on vs code create table code
- Firewall rule "0.0.0.0" was added as previous rule was not validating the IP of Data Factory. This rule allows access to SQL DB from any IP - great for dev not prod. Private endpoint integration and security added in phase 6 