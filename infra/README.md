# azure-banking-data-platform
Azure data platform simulating a bank's transaction and reporting pipeline


# Infra
## Storage Account Setup
- Created ADLS Gen2 storage to create hierarchical namespace allowing for permissions to be given to users based on folders
- TLS 1.2 used for secure encryption and compliance
- LRS for dev purposes
- Private access to containers
- Designed to support a medallion structure
    - **bronze** -> raw ingested API data
    - **silver** -> cleaned and transformed data 
    - **gold** -> curated for user dashboards and other analytics
- Storage is structured to support scalable ingestion pipelines and role based access control

## Function App & Identity Setup
- Created `cibc-nhl-ingest-func` on a Linux consumption plan to handle scheduled ingestion from the NHL API
- App Insights and App Service Plan are auto-provisioned by Azure on creation
- Function is inactive until code is deployed. Security and network hardening deferred to later production
- Assigned a System-assigned Managed Identity to the Function App
    - Granted `Storage Blob Data Contributor` RBAC role scoped to the storage account
    - Allows the function to write to bronze container without storing credentials in code
