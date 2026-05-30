# Transform

## bronze_to_silver
- reads the latest json file from the bronze container using dynamic file listing
- Explodes nested "games" array into a flattened structure using Pyspark
- Selects and aliases key field such as gameid, date, teams, scores
- adds custom CGY columns such as CGYScore, OpponentScore, CGYWin using `when/otherwise` logic
- Writes to silver blob container as a delta table 

## Why a delta format?
- ACID transactions have no partial or corrupt writes if the pipeline fails - keeps all data intact. Great for banking transactions
- Schema enforcement rejects bad data automatically
- Audit logs are all tracked which is also great for banking
- No other formats like parquet, csv, or json uses acid, being able to rollback with time travel, or auditing


## Development Approach
- Notebook must be attached to a cluster. Serverless compute does not support a custom Spark config or ADLS authentication
-  Troubleshooting included disabling photon acceleration, using account key from storage, runtime version changes - root cause was running serverless instead of configured cluster 
- once notebook logic for all transformations has been configured, an automated pipeline will be added to convert notebooks to datebricks jobs on a schedule