import requests
import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os
import azure.functions as func

load_dotenv()
account_url = os.getenv("ACCOUNT_URL")
credentials = DefaultAzureCredential()

# connects to container and creates and uploads the blob with API data 
def upload_blob(filename, req):
    # variable to connect to bronze container
    container_name = 'bronze'
    
    # using blob_service_client to connect to the container to upload 
    blob_service_client = BlobServiceClient(account_url=account_url, credential = credentials)
    container_client = blob_service_client.get_container_client(container = container_name)
    
    # specifies blob name and the data within the blob
    container_client.upload_blob(name = filename, data = req)

# GET request is retrieved from API, converted from raw -> JSON and passed to upload_blob function
# timer is retrieved from function.json (Azure Managed, hence no import) 
def main(mytimer: func.TimerRequest) -> None:
    req = requests.get("https://api-web.nhle.com/v1/club-schedule-season/CGY/now")
    data = json.dumps(req.json())
    filename = f"nhl-cgy-{datetime.now().strftime('%Y-%m-%d-%H-%M')}.json"
    
    upload_blob(filename, data)
    
# for local testing
if __name__ == "__main__":
    main(None)

