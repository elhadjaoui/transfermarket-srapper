# import logging
# logging.basicConfig(filename='storage_manager.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

import os
import dotenv
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import requests
from requests.exceptions import RequestException

dotenv.load_dotenv()

def upload_photo_to_azure(photo_url, player_id,logging):
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_CONNECTION_STRING'))
    container_client = blob_service_client.get_container_client(os.getenv("CONTAINER_NAME"))
    if container_client.exists() == False:
        logging.info(f"Container {os.getenv('CONTAINER_NAME')} does not exist. Creating...")
        container_client.create_container()
        logging.info(f"Container {os.getenv('CONTAINER_NAME')} created.")
    try:
        response = requests.get(photo_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        blob_name = f"{player_id}.jpg"
        blob_client = blob_service_client.get_blob_client(os.getenv("CONTAINER_NAME"), blob_name)
        
        # Upload the blob
        blob_client.upload_blob(response.content, blob_type="BlockBlob")
        logging.info(f"Blob {blob_name} uploaded to Azure.")
        return blob_client.url

    except RequestException as e:
        logging.info(f"Error fetching photo from URL: {e}")
        return ""
    except ResourceExistsError:
        logging.info(f"Blob {blob_name} already exists.")
        return blob_client.url
    except Exception as e:
        logging.info(f"Error uploading to Azure: {e}")
        return ""

# upload_photo_to_azure("https://img.a.transfermarkt.technology//header/480267-1662586164.jpg?lm=1", 1234)