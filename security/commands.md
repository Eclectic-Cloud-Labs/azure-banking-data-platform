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
### sqlAuthPass
az keyvault secret set --name sqlAuthPass --vault-name gurbovault --value <sqlAuthPass>

## Link KeyVault Service in ADF and remove a manual entry of the SP id and secret
see ./serve for update

## Create KeyVault Secrets role for adf 
az role assignment create --role "Key Vault Secrets User" --assignee <adf-principal-id> --scope /subscriptions/<subscription-id>/resourceGroups/apiRG/providers/Microsoft.KeyVault/vaults/gurbovault

## Create VNET for Private Endpoint (realized i didnt need as adf does that with managed vnet)
az network vnet create --name gurbovnet -g apiRG --address-prefixes 10.0.0.0/16 --subnet-name subnet1 --subnet-prefixes 10.0.0.0/24

## Create Private Endpoint for ADF connection to SQL Server
az network private-endpoint create --connection-name adfConnectSQL --name gurboVnetPrivEndpoint -g apiRG --vnet-name gurbovnet --subnet subnet1 --private-connection-resource-id /subscriptions/<Subscription-id>/resourceGroups/apiRG/providers/Microsoft.Sql/servers/nhl-gurbo-sql-server --group-id sqlServer

## Delete previously created firewall rules for SQL Server
az sql server firewall-rule delete --name AllowDataFactory --resource-group apiRG --server nhl-gurbo-sql-server
az sql server firewall-rule delete --name AllowMyIp  --resource-group apiRG --server nhl-gurbo-sql-server
az sql server update --name nhl-gurbo-sql-server --resource-group apiRG --enable-public-network false

## Create Private DNS Zone 
az network private-dns zone create -g apiRG --name privatelink.database.windows.net

## Create VNET Link
az network private-dns link vnet create --name sqlDnsLink --registration-enabled false --resource-group apiRG --virtual-network gurbovnet --zone-name privatelink.database.windows.net