import os
from utils import get_blob_service_client

def upload_country_currency():
    local_file_path = "data/tmp/tradecorp_raw/reference/country_currency.csv"
    
    blob_service_client = get_blob_service_client()
    container_name = "raw"
    blob_name = "reference/country_currency.csv"
    
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
        
    print(f"Fichier country_currency.csv uploadé avec succès vers {container_name}/{blob_name}")

if __name__ == "__main__":
    upload_country_currency()