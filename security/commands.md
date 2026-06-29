# Security

## Register KeyVault Namespace
az provider register --namespace Microsoft.KeyVault
## Create KeyVault
az keyvault create --resource-group apiRG --enable-rbac-authorization true --location eastus --name gurbovault
## Assign Me the Correct Role 
az role assignment create --role "Key Vault Administrator" --scope /subscriptions/<subscription-id>/resourceGroups/apiRG/providers/Microsoft.KeyVault/vaults/gurbovault --assignee <object-id>
## Create Secret
### sp-client-id
az keyvault secret set --name sp-client-id --vault-name gurbovault --value <sp-client-id>
### sp-client-secret
az keyvault secret set --name sp-client-secret --vault-name gurbovault --value <sp-client-secret>
### sp-tenant-id
az keyvault secret set --name sp-tenant-id --vault-name gurbovault --value <sp-tenant-id>

## Link KeyVault Service in ADF and remove a manual entry of the SP id and secret

## Create KeyVault Secrets role for adf 
az role assignment create --role "Key Vault Secrets User" --assignee <keyvault-principal-id> --scope /subscriptions/<subscription-id>/resourceGroups/apiRG/providers/Microsoft.KeyVault/vaults/gurbovault