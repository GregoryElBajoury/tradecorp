import io
import os
import pandas as pd
from azure.storage.blob import BlobServiceClient

# Récupération directe des variables
account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

connect_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

container_client = blob_service_client.get_container_client("clean")
blob_client = container_client.get_blob_client(
    "tradecorp_enriched/part-00000-d5d643c7-e8f0-4c03-bcfa-938fe63aa574-c000.snappy.parquet"
)

stream = io.BytesIO(blob_client.download_blob().readall())
df = pd.read_parquet(stream)

print(df.head())
print(f"Nombre de lignes : {len(df)}")