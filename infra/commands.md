**Azure Cloud Lab**

# Storage Account Setup
- login: az login --use-device-code

## Create Resource Group
az group create --name apiRG --location eastus

## Create Storage Account
az storage account create --resource-group apiRG --name gurboapistorage --location eastus --sku Standard_LRS --kind StorageV2 --min-tls-version TLS1_2 --allow-blob-public-access false --enable-hierarchical-namespace true

az storage account show --name gurboapistorage --resource-group apiRG

## Create Containers
az storage container create --name bronze --account-name gurboapistorage --auth-mode login
az storage container create --name silver --account-name gurboapistorage --auth-mode login
az storage container create --name gold --account-name gurboapistorage --auth-mode login