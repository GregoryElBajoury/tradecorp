import os
from pyspark.sql import DataFrame, SparkSession
from utils import get_blob_service_client


def upload_directory_to_azure(blob_service_client, container_name: str, local_dir: str, remote_dir: str):
    """Parcourt un dossier local (contenant les fichiers Parquet de Spark) et les envoie vers Azure."""
    container_client = blob_service_client.get_container_client(container_name)
    
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_dir)
            blob_name = os.path.join(remote_dir, relative_path).replace("\\", "/")
            
            blob_client = container_client.get_blob_client(blob_name)
            with open(local_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            print(f"Fichier Parquet transféré vers clean : {blob_name}")


def write_clean_data_to_azure(df: DataFrame, container_name: str = "clean", dataset_name: str = "tradecorp_enriched"):
    """Exporte le DataFrame en Parquet localement puis l'envoie dans le conteneur clean."""
    blob_service_client = get_blob_service_client()
    
    local_tmp_path = f"/home/jovyan/data/tmp/{dataset_name}"
    
    # 1. Écriture du DataFrame en Parquet localement par Spark
    print(f"Écriture du DataFrame en Parquet local : {local_tmp_path}")
    df.write.mode("overwrite").parquet(local_tmp_path)
    
    # 2. Envoi vers ADLS Gen2 (zone clean)
    print(f"Téléversement vers le conteneur Azure '{container_name}'...")
    upload_directory_to_azure(blob_service_client, container_name, local_tmp_path, remote_dir=dataset_name)
    
    print(f"Export de '{dataset_name}' terminé avec succès dans la zone clean !")


if __name__ == "__main__":
    # Test unitaire isolé du writer avec un faux DataFrame
    spark = SparkSession.builder \
        .appName("TradeCorpWriterTest") \
        .getOrCreate()

    data = [("1", "Test Produit", 15.0)]
    columns = ["product_id", "product_name", "prix_unitaire"]
    test_df = spark.createDataFrame(data, columns)
    
    write_clean_data_to_azure(test_df, container_name="clean", dataset_name="test_dataset")