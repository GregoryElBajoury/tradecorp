import os
from pyspark.sql import DataFrame, SparkSession
from utils import download_blob_to_local, get_blob_service_client


def load_raw_data_to_spark(spark: SparkSession, container_name: str = "raw") -> dict:
    """Télécharge explicitement les fichiers métier et de référence depuis ADLS Gen2 et les charge dans Spark."""
    blob_service_client = get_blob_service_client()
    
    # 1. Les 8 fichiers métier CSV
    file_names = [
        "categories.csv",
        "customers.csv",
        "employees.csv",
        "order_details.csv",
        "orders.csv",
        "products.csv",
        "shippers.csv",
        "suppliers.csv"
    ]
    
    local_data_dir = "/home/jovyan/data/tmp/tradecorp_raw"
    os.makedirs(local_data_dir, exist_ok=True)
    
    dfs = {}
    
    for file_name in file_names:
        local_path = os.path.join(local_data_dir, file_name)
        download_blob_to_local(blob_service_client, container_name, file_name, local_path)
        
        table_key = file_name.replace(".csv", "")
        dfs[table_key] = (
            spark.read.option("header", "true")
                      .option("inferSchema", "true")
                      .csv(local_path)
        )
        print(f"Fichier chargé explicitement : {file_name} -> DataFrame['{table_key}']")

    # 2. Les fichiers de référence (CSV et JSON)
    reference_files = {
        "country_currency": "reference/country_currency.csv",
        "exchange_rates": "reference/exchange_rates.json"
    }

    local_ref_dir = os.path.join(local_data_dir, "reference")
    os.makedirs(local_ref_dir, exist_ok=True)

    for key, blob_path in reference_files.items():
        local_ref_path = os.path.join(local_data_dir, blob_path)
        download_blob_to_local(blob_service_client, container_name, blob_path, local_ref_path)

        if blob_path.endswith(".csv"):
            dfs[key] = (
                spark.read.option("header", "true")
                          .option("inferSchema", "true")
                          .csv(local_ref_path)
            )
        elif blob_path.endswith(".json"):
            dfs[key] = spark.read.json(local_ref_path)
            
        print(f"Référence chargée : {blob_path} -> DataFrame['{key}']")
            
    return dfs


if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("TradeCorpReaderTest") \
        .getOrCreate()

    print("Début du chargement des fichiers métier et de référence depuis ADLS Gen2...")
    dfs = load_raw_data_to_spark(spark)
    
    print(f"\nChargement terminé ! {len(dfs)} DataFrames créés :")
    for table_name, df in dfs.items():
        print(f" - {table_name} : {df.count()} lignes")