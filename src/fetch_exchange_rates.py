import requests
from utils import get_blob_service_client

def fetch_and_upload_exchange_rates():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    
    # 1. Appel de l'API gratuite
    response = requests.get(url)
    response.raise_for_status()
    raw_json = response.text  # Réponse JSON brute

    # 2. Initialisation du client ADLS Gen2 via utils.py
    blob_service_client = get_blob_service_client()
    
    # Définition du conteneur et du chemin cible
    container_name = "raw"
    blob_name = "reference/exchange_rates.json"
    
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # 3. Upload du JSON brut vers Azure
    blob_client.upload_blob(raw_json, overwrite=True)
    
    print(f"Taux de change récupérés et uploadés avec succès vers {container_name}/{blob_name}")

if __name__ == "__main__":
    fetch_and_upload_exchange_rates()