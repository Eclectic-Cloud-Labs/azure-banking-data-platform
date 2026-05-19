**Azure Cloud Lab**


## Create Function App
az functionapp create --name cibc-nhl-ingest-func --resource-group apiRG --storage-account gurboapistorage --consumption-plan-location eastus --runtime python --runtime-version 3.11 --os-type Linux --functions-version 4

## Enable Managed Identity and Assign RBAC Role
az functionapp identity assign -g apiRG --name cibc-nhl-ingest-func
    - MI used over storage account keys to avoid storing credentials in code while allowing the same functionality
    - MI authenticates through Azure AD with no secrets required while preventing leaks through repos/logs

# Get Principal ID
az functionapp show -g apiRG --name cibc-nhl-ingest-func --query identity.principalId --output tsv

# Get Subscription ID
az account show --query id --output tsv

# Assign Storage Blob Data Contributor to MI
az role assignment create --assignee <principalId> --role "Storage Blob Data Contributor" --scope /subscriptions/<subscriptionId>/resourceGroups/apiRG/providers/Microsoft.Storage/storageAccounts/gurboapistorage

## Local Development Setup (VS Code)
python -m venv .venv
source .venv/Scripts/activate
pip install python-dotenv azure-storage-blob

## requirements.txt
azure-storage-blob
python-dotenv
requests
    - Azure Functions needs to know which packages to install when my code is deployed. Without this file, my function runs with no libraries and will fail
    