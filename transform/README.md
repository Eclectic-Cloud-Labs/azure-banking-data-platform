# Transform

## bronze_to_silver
- Reads the latest json file from the bronze container using dynamic file listing
- Explodes nested "games" array into a flattened structure using Pyspark
- Selects and aliases key field such as gameid, date, teams, scores
- Adds custom CGY columns such as CGYScore, OpponentScore, CGYWin using `when/otherwise` logic
- Writes to silver blob container as a delta table 
*update1*
- Addition of "OpponentTeamName" in the bronze_to_silver notebook was needed for an aggregated column

## silver_to_gold
- Retrieval of SP id, secret, and tenantId is still needed for every cluster startup 
- Pulled data from silver blob - no sort function needed because of delta format (see below)
- Transformed data into 2 different aggregated states (W/L for CGY, and GoalDifferential), then wrote to gold container as a delta format once again

## Databricks Jobs & Pipeline Automation
- Created a Databricks Job with two dependent tasks — `bronze_to_silver` runs first, `silver_to_gold` only runs if `bronze_to_silver` succeeds
- Scheduled at `0 30 6/12 * * *` — fires at 6:30 AM and 6:30 PM UTC (12:30 AM and PM Mountain)
- Aligns with Function App ingestion schedule — 30 minute buffer gives bronze time to land before transformation starts

### Why Jobs over interactive notebooks
- Notebooks are for development while jobs are for production
- Job clusters spin up fresh when scheduled, run, then terminate resulting in lower cost than keeping an all purpose cluster running
- Dependency chain ensures bad data never reaches gold. If bronze fails, silver and gold don't run
 

### Why all succeeded dependency in databricks
- All levels are modular (high availabilty and observability)
- Without dependency, if bronze wrote corrupt or incomplete data, silver would transform bad data into gold
- Fail fast at the source rather than propagating bad data downstream
- Same principle banks use for pipeline reliability where one bad stage should never silently corrupt the next

### Why a delta format?
- ACID transactions have no partial or corrupt writes if the pipeline fails - keeps all data intact. Great for banking transactions
- Schema enforcement rejects bad data automatically
- Audit logs are all tracked which is also great for banking
*update1*
- Parquet lacks ACID transactions, time travel, and audit logs - Delta adds all of these on top of Parquets columnar storage
- Delta automatically reads the latest version of the table via its transaction log so no manual file management needed

## Development Approach
- Notebook must be attached to a cluster. Serverless compute does not support a custom Spark config or ADLS authentication
    -  Troubleshooting included disabling photon acceleration, using account key from storage, runtime version changes - root cause was running serverless instead of configured cluster 
    - Prod environment requires unity catalog where a startup is not necessary - Unity Catalog would serve it more efficiently/on demand
- Once notebook logic for all transformations has been configured, an automated pipeline will be added to convert notebooks to databricks jobs on a schedule
