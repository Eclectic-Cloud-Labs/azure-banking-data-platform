## KQL 
### Successful runs per pipeline
ADFActivityRun
| where OperationName contains "succeeded"
| summarize count() by OperationName

### Unsuccessful Blob Storage runs
StorageBlobLogs
| where StatusText != "Success"
| where StatusText != "ContainerAlreadyExists"
| order by TimeGenerated desc

### Successful Bronze Blob Storage Writes
StorageBlobLogs
| where OperationName == "PutBlob"
| where Uri contains "bronze"
| order by TimeGenerated desc  

### SQL DB Errors 
AzureDiagnostics
| where ResourceType == "SERVERS/DATABASES"
| where Category == "Errors"
| where Message !contains "sys.dm_os_windows_info"
| where Message !contains "sys.sql_logins"

### Data Freshness SLI 
StorageBlobLogs
| where OperationName == "PutBlob"
| where Uri contains "bronze"
| top 1 by TimeGenerated
| extend MinutesSinceLastWrite = datetime_diff('minute', now(), TimeGenerated)
| extend ScheduledHour = iff(hourofday(TimeGenerated) < 12, 0, 12)
| extend ExpectedRunTime = make_datetime(datetime_part('year', TimeGenerated), datetime_part('month', TimeGenerated), datetime_part('day', TimeGenerated), ScheduledHour, 0, 0)
| extend SecondsPastSchedule = datetime_diff('second', TimeGenerated, ExpectedRunTime)
| project TimeGenerated, MinutesSinceLastWrite, SecondsPastSchedule

### Pipeline Reliability SLI
ADFActivityRun
| where OperationName !contains "InProgress"
| where OperationName !contains "Queued"
| summarize 
    TotalRuns = count(),
    SuccessfulRuns = countif(OperationName contains "Succeeded")
| extend SuccessRate = (SuccessfulRuns * 100.0) / TotalRuns

### SQL Query Performance SLI
AzureDiagnostics
| where ResourceType == "SERVERS/DATABASES"
| where duration_d >= 2000000 
| project duration_d, TimeGenerated, query_id_d