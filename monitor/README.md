# Azure Monitor, Logs,  Queries - PHASE 5


## Whats Been Built 
- Created a Log Analytics Workspace and connected all relevant resources (ADF, ADLS Gen2)


## Monitor and Reliability
### Log Analytics Workspace
- Created 'gurboLogAnalyticSpace' as the central log store. All resource diagnostic logs flow here
- Enables cross resource querying via KQL from a single location instead of checking each resource individually


## Diagnostic Settings
Connected the following resources to the Log Analytics workspace using portal to retrieve all relevent logs:
- **Azure Functions** - FunctionAppLogs and AllMetrics. Captures function execution, errors, and runtime health
- **ADLS Gen2** - StorageRead, StorageWrite, StorageDelete on the blob sub-resource. Captures all data layer operations
- **Azure Data Factory** - PipelineRuns, TriggerRuns, ActivityRuns. Captures full pipeline execution history
- **Azure SQL Database** - Errors, QueryStoreRuntimeStatistics, QueryStoreWaitStatistics, Timeouts, Blocks, Deadlocks. Captures query performance and connection health
- **Databricks** - configured and saved for Phase 7 when workspace is recreated

### Why resource-specific mode
- '--export-to-resource-specific true' stores logs in dedicated tables per resource type instead of a generic 'AzureDiagnostics' catch-all
- Makes KQL queries faster and cleaner - query 'ADFActivityRun' directly instead of filtering a massive shared table
- Standard practice in enterprise Azure environments


## Alerts
Created five alert rules connected to the 'cibc-nhl-ops-team' action group:
- **FunctionAppServerError** - HTTP server errors > 1, evaluated every 1 min with 5 min lookback. Severity: 1
- **FunctionAppNotRunning** - Function execution count < 1, evaluated every 1 hour with 12 hour lookback. Severity 1
- **StorageIssue** - Transaction anomaly detection using dynamic threshold, evaluated every 10 min with 1 hour lookback. Severity 3
- **PipelineNotWorking** - Failed ADF pipeline runs > 0, evaluated every 1 min with 5 min lookback. Severity 0
- **DatabaseUnderSiege** - Failed SQL connections > 1, evaluated every 1 min with 5 min lookback. Severity 1

### Why dynamic threshold for storage
- Storage transaction volume varies naturally - more activity during ingestion windows, near zero otherwise
- Static threshold would generate false positives during normal low-activity periods


## KQL Queries (monitor\queries.md)
### Successful runs per pipeline
- Finds logs of all the successful runs per pipeline. Info is aggregated by a single number per pipeline, which can be correlated to how many times it should be running per day
- Showed 2 different numbers as 2 different pipelines were created in ADF

### Unsuccessful Blob Storage runs
- Finds logs of all unsuccessful runs
- | where StatusText != 'ContainerAlreadyExists' - was used to filter out all instances of Azure trying create a new container from FunctionApp to retrieve all real unsuccessful runs. 
- So far no unsuccessful runs 

### Successful Bronze Blob Storage Writes
- Finds all successful PutBlob operations to the bronze container. This confirms NHL ingestion is running on schedule from API
- Filters by 'OperationName == "PutBlob"' and 'Uri contains "bronze"' to isolate actual data writes from internal Azure Functions storage operations
- Auth type 'OAuth' on all entries confirms Managed Identity is authenticating correctly and not account keys
- Response sizes vary per run. Larger payloads indicate more game data returned from the NHL API on that day

### SQL DB Errors
- Queries 'AzureDiagnostics' filtered to SQL Database error category to surface any failed queries or connection issues
- Filters out known Azure internal system view errors ('sys.dm_os_windows_info', 'sys.sql_logins') which are expected in Azure SQL PaaS and would otherwise create noise
- No real application errors found. This confirms database is healthy and ADF copy operations are completing without SQL-level failures


## SLIs & SLOs

### Why define SLIs and SLOs
At a bank, internal data platforms directly support business decisions such as risk assessments, reporting, and client recommendations all depend on accurate and efficient data. Without defining reliability targets, there's no objective way to know if the platform is meeting business expectations or silently degrading

### SLI 1 - Data Freshness
- **SLI:** Time elapsed since last successful bronze write and checks if the storage hasn't been written to in more than 10 minutes
- **SLO:** Gold data must be refreshed within 10 minutes of each scheduled pipeline run
- **Error Budget:** Zero tolerance - a missed run means analysts are working with data that is at minimum 12 hours stale, which is unacceptable for time-sensitive reporting
- **Why:** If the pipeline misses a run and data is stale, business decisions downstream are based on outdated information. At a bank that directly impacts risk assessments and client-facing recommendations.

### SLI 2 - Pipeline Reliability
- **SLI:** Successful pipeline runs / total pipeline runs
- **SLO:** 99.9% success rate
- **Error Budget:** ~1 failure per 1,000 runs - at 60 runs/month that's roughly 1 allowed failure every 16 months
- **Why:** Set at 99.9% rather than 99.99% because a single missed run on an internal analytics pipeline is recoverable within the next 12 hour cycle. Payment processing would require 99.99% - the impact of a failed analytics run is lower but still demands near-zero tolerance given the downstream business dependency.

### SLI 3 - Query Performance
- **SLI:** SQL query execution time for gold layer reporting queries
- **SLO:** 99% of queries must complete within 2 seconds
- **Error Budget:** 1% of queries can exceed 2 seconds before breach
- **Why:** Internal analysts querying standings and goal differential expect near-instant results. Slow queries erode trust in the platform and signal underlying performance issues - poor indexing, table bloat, or resource contention - that compound over time if left unmonitored.