import requests
import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os

load_dotenv()
account_url = os.getenv("ACCOUNT_URL")
credentials = DefaultAzureCredential()

def upload_blob():
    local_dir = "data"
    container_name = 'bronze'
    
    blob_service_client = BlobServiceClient(account_url=account_url, credential = credentials)
    container_client = blob_service_client.get_container_client(container = container_name)
    
    filenames = os.listdir(local_dir)
    
    for filename in filenames:
        full_file_path = os.path.join(local_dir, filename)
        with open(full_file_path, "r") as fl:
            data = fl.read()
            container_client.upload_blob(name = filename, data = data)

if __name__ == "__main__":
    req = requests.get("https://api-web.nhle.com/v1/club-schedule-season/CGY/now")
    local_dir = 'data'
    filename = f"nhl-cgy-{datetime.now().strftime('%Y-%m-%d-%H')}.json"
    full_file_path = os.path.join(local_dir, filename)
    with open(full_file_path, "w") as file:
        json.dump(req.json(), file, indent=4)
    
    upload_blob()
        
    

