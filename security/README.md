# Security & Access

## What was built
- Azure Key Vault for centralized secret management
- Private networking for ADF-to-SQL connectivity using managed private endpoints (in progress)
- VNet and private DNS zone for future resource isolation 
- Removed broad public firewall access from SQL Server


## Azure Key Vault
- Created 'gurbovault' with RBAC authorization enabled
- Stored SP credentials and SQL admin credentials as secrets:
  - 'sp-client-id'
  - 'sp-client-secret'
  - 'sp-tenant-id'
  - SQL admin credentials
- Assigned 'Key Vault Secrets User' role to ADF's Managed Identity so pipelines can fetch credentials at runtime
- Updated ADF ADLS Gen2 and SQL Server linked service to pull SP secret and SQL admin credentials from Key Vault instead of storing it directly in ADF config

### Why Key Vault over hardcoded credentials
- Credentials in ADF linked service JSON files get committed to GitHub - Key Vault references replace the value with a pointer, never the secret itself
- Every secret access is logged such as who, when, and from where. Required for banking compliance audits
- Secrets can be rotated in Key Vault without touching ADF config or redeploying anything


## Private Networking
### VNet & Subnet
- Created 'gurbovnet' with address space '10.0.0.0/16' and subnet '10.0.0.0/24'
- Foundation for private connectivity - resources deployed into this VNet can communicate privately

### SQL Server Private Endpoint
- Created private endpoint 'gurboVnetPrivEndpoint' on SQL Server inside 'gurbovnet'
- Gives SQL Server a private IP ('10.0.0.x') accessible only from within the VNet
- Removed 'AllowAzureServices' ('0.0.0.0') firewall rule - public access disabled

### Private DNS Zone
- Created 'privatelink.database.windows.net' DNS zone and linked to 'gurbovnet'
- Resolves 'nhl-gurbo-sql-server.database.windows.net' to the private IP for any resource inside 'gurbovnet'
- Prepared for future VNet-connected resources - not required for ADF which uses its own managed VNet

### ADF Managed VNet Integration Runtime
- Switched ADF from public integration runtime to managed VNet IR
- ADF compute now runs inside Microsoft's managed VNet which allows no public internet access 
- Created managed private endpoints inside ADF's managed VNet for both ADLS Gen2 and SQL Server
- Both connections approved and ADF routes all data movement through private network (in progress because of archived files from the previous phase)

### Why managed VNet IR over public IR
- Public IR means ADF traffic crosses the public internet which is unacceptable for banking data
- Managed VNet IR keeps all traffic on Microsoft's private backbone
- Required for private endpoint connectivity from ADF
- Replaces the '0.0.0.0' SQL firewall rule with Zero Trust network architecture


## Known Issue
- Gold Delta files in ADLS Gen2 moved to archive tier by lifecycle policy. Databricks workspace was deleted after Phase 3 so files haven't been modified in over 14 days
- ADF pipeline will succeed once Databricks is recreated in Phase 7 and gold data is refreshed
- Architecture is correct. Only issue is data availability. Not a configuration issue


## Development Approach & Troubleshooting
### Connecting ADF to SQL Server Privately
The challenge was getting ADF to reach SQL Server without public internet exposure. The solution required many interconnected pieces:

1. Created a private endpoint on SQL Server which required a VNet, private DNS zone, and VNet link first
    - Initially assumed ADF would route through 'gurbovnet' private endpoint and DNS zone to reach SQL Server. Initial assumption was that ADF would connect to the private DNS instead of fully using its own Microsoft managed VNet. The private endpoint, DNS zone, and VNet link created for SQL Server in 'gurbovnet' were not actually used by ADF. 
2. ADF was outside the VNet so it couldn't use that private endpoint directly - needed a Managed VNet Integration Runtime inside ADF Studio
3. After creating the IR, all linked services (ADLS Gen2 and SQL Server) had to be updated to use the new IR as provisioning alone doesn't activate it (if only I knew)
4. Created managed private endpoints inside ADF's managed VNet pointing to SQL Server and ADLS Gen2
5. After creating the SQL managed private endpoint, it required manual approval on the SQL Server side - portal -> SQL Server -> Security -> Networking -> Private Access -> Approve

### Mistakes Made
- Initially reused the ADLS Gen2 linked service private endpoint on ADF for SQL Server. Each resource needs its own dedicated managed private endpoint inside ADF
- Created a private DNS zone for storage which wasn't needed. ADF's managed VNet handles DNS resolution internally for managed private endpoints

### Root Cause of Pipeline Failure
After all networking was configured correctly, the ADF pipeline still failed with a Parquet read error. The cause after troubleshooting was gold Delta files in ADLS Gen2 had been moved to **archive tier** by the lifecycle management policy :(. Databricks was deleted after Phase 3 so the gold files hadn't been modified in over 14 days. Archive tier blobs are offline and cannot be read until rehydrated. Pipeline architecture is correct - data will be accessible once Databricks is recreated in Phase 7 and gold files are refreshed to hot tier.


