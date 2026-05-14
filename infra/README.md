# azure-banking-data-platform
Azure data platform simulating a bank's transaction and reporting pipeline


# Infra
- Created ADLS Gen2 storage to create hierarchical namespace allowing for permissions to be given to users based on folders
- TLS 1.2 used for secure encryption and compliance
- LRS for dev purposes
- Private access to containers
- Designed to support a medallion structure
    - **bronze** -> raw ingested API data
    - **silver** -> cleaned and transformed data 
    - **gold** -> curated for user dashboards and other analytics
- Storage is structured to support scalable ingestion pipelines and role based access control