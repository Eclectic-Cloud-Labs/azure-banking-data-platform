
az monitor log-analytics workspace create --name gurboLogAnalyticSpace -g apiRG --location eastus

## Connect FunctionApp Diagnostic Settings to Workspace
az monitor diagnostic-settings create --name functionapp-diag-settings --resource /subscriptions/SUBSCRIPTION_ID/resourceGroups/apiRG/providers/Microsoft.Web/sites/cibc-nhl-ingest-func --logs '[{"category":"FunctionAppLogs","enabled":true}]' --metrics '[{"category":"AllMetrics","enabled":true}]'--workspace /subscriptions/SUBSCRIPTION_ID/resourceGroups/apiRG/providers/Microsoft.OperationalInsights/workspaces/gurboLogAnalyticSpace --export-to-resource-specific true
 
## Connect Storage account to workspace
az monitor diagnostic-settings create --name storage-diag-settings --resource /subscriptions/SUBSCRIPTION_ID/resourceGroups/apiRG/providers/Microsoft.Storage/storageAccounts/gurboapistorage/blobServices/default --logs '[{"category":"StorageRead","enabled":true},{"category":"StorageWrite","enabled":true},{"category":"StorageDelete","enabled":true}]' --metrics '[{"category":"AllMetrics","enabled":true}]' --workspace /subscriptions/SUBSCRIPTION_ID/resourceGroups/apiRG/providers/Microsoft.OperationalInsights/workspaces/gurboLogAnalyticSpace --export-to-resource-specific true

## Data factory 
### Find correct log names
az monitor diagnostic-settings categories list --resource /subscriptions/SUBSCRIPTION_ID/resourceGroups/apirg/providers/Microsoft.DataFactory/factories/gurbo-nhl-factory

az monitor diagnostic-settings create --name datafactory-diag-settings --resource /subscriptions/SUBSCRIPTION_ID/resourceGroups/apirg/providers/Microsoft.DataFactory/factories/gurbo-nhl-factory --logs '[{"category":"ActivityRuns","enabled":true},{"category":"PipelineRuns","enabled":true},{"category":"TriggerRuns","enabled":true}]' --metrics '[{"category":"AllMetrics","enabled":true}]' --workspace /subscriptions/SUBSCRIPTION_ID/resourceGroups/apiRG/providers/Microsoft.OperationalInsights/workspaces/gurboLogAnalyticSpace --export-to-resource-specific true

## sql db 
### Find correct Log names
az monitor diagnostic-settings categories list --resource /subscriptions/SUBSCRIPTION_ID/resourceGroups/apiRG/providers/Microsoft.Sql/servers/nhl-gurbo-sql-server/databases/nhl-gurbo-db   

az monitor diagnostic-settings create --name sqldb-diag-settings --resource /subscriptions/SUBSCRIPTION_ID/resourceGroups/apiRG/providers/Microsoft.Sql/servers/nhl-gurbo-sql-server/databases/nhl-gurbo-db --logs '[{"category":"SQLInsights","enabled":true},{"category":"QueryStoreRuntimeStatistics","enabled":true},{"category":"QueryStoreWaitStatistics","enabled":true},{"category":"Errors","enabled":true},{"category":"DatabaseWaitStatistics","enabled":true},{"category":"Timeouts","enabled":true},{"category":"Blocks","enabled":true},{"category":"Deadlocks","enabled":true}]' --workspace /subscriptions/SUBSCRIPTION_ID/resourceGroups/apiRG/providers/Microsoft.OperationalInsights/workspaces/gurboLogAnalyticSpace --export-to-resource-specific true


## databricks (when its recreated in phase 7)




az monitor diagnostic-settings create --name databricks-diag-settings --resource /subscriptions/SUBSCRIPTION_ID/resourceGroups/apiRG/providers/Microsoft.Databricks/workspaces/gurbosbricks --logs '[{"category":"dbfs","enabled":true},{"category":"clusters","enabled":true},{"category":"accounts","enabled":true},{"category":"jobs","enabled":true},{"category":"notebook","enabled":true},{"category":"ssh","enabled":true},{"category":"workspace","enabled":true},{"category":"secrets","enabled":true},{"category":"sqlPermissions","enabled":true}]' --workspace /subscriptions/SUBSCRIPTION_ID/resourceGroups/apiRG/providers/Microsoft.OperationalInsights/workspaces/gurboLogAnalyticSpace --export-to-resource-specific true