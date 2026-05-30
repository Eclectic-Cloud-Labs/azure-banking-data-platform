# Databricks Setup

## Create service principal for ADLS Access
az ad sp create-for-rbac --name cibc-nhl-sp --role "Storage Blob Data Contributor" --scopes /subscriptions/<subscriptionId>/resourceGroups/apiRG/providers/Microsoft.Storage/storageAccounts/gurboapistorage

## Install databricks cli
pip install databricks-cli
winget install Databricks.DatabricksCLI

## Configure databricks cli
databricks configure --token

## Create secret scope
databricks secrets create-scope --scope adls-scope

## Store service principal credentials
databricks secrets put-secret adls-scope sp-client-id --string-value <appId>
databricks secrets put-secret adls-scope sp-client-secret --string-value <password>
databricks secrets put-secret adls-scope sp-tenant-id --string-value <tenantId>
databricks secrets put-secret adls-scope storage-account-key --string-value <key1>

## Verify secrets
databricks secrets list-secrets adls-scope

## Why service principal over managed identity
- Databricks control plane is partially managed by Databricks, not fully within Azure
- SP credentials can be explicitly configured in Databricks Secrets
- MI support in Databricks requires Unity Catalog setup — deferred to Phase 7
- SP + Databricks Secrets is the standard pattern in enterprise Databricks environments

