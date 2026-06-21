# Serve Commands

## Azure SQL Server & Database
az sql server create --name nhl-gurbo-sql-server --resource-group apiRG --admin-user gk --admin-password <password> --location canadacentral
az sql db create -g apiRG --server nhl-gurbo-sql-server --name nhl-gurbo-db --edition Basic --capacity 5

## Firewall Rules
# Allow local machine
az sql server firewall-rule create -g apiRG --server nhl-gurbo-sql-server --name AllowMyIp --start-ip-address MY_IP_ADDRESS --end-ip-address MY_IP_ADDRESS

# Allow Data Factory integration runtime
az sql server firewall-rule create -g apiRG --server nhl-gurbo-sql-server --name AllowDataFactory --start-ip-address 20.42.3.136 --end-ip-address 20.42.3.136

## Azure Data Factory
az datafactory create --factory-name gurbo-nhl-factory --resource-group apiRG --location eastus

## SQL Tables
CREATE TABLE WL (
    id INT IDENTITY(1,1) PRIMARY KEY,
    Wins int,
    Losses int
);

CREATE TABLE GOALDIFF (
    id INT IDENTITY(1,1) PRIMARY KEY,
    OpponentTeamName VARCHAR(100),
    OpponentGoalDiff int
);