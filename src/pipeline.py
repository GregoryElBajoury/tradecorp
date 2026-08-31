from pyspark.sql import SparkSession
from reader import read_csv
from transformer import (
    clean_customers,
    clean_orders,
    clean_order_details,
    add_sous_total
)
from writer import write_parquet

def main():
    # 1. Initialisation de la SparkSession
    spark = SparkSession.builder \
        .appName("TradeCorp-ETL-Pipeline") \
        .getOrCreate()

    # Définition des chemins d'accès (dossier raw et dossier de sortie processed/tmp)
    raw_path = "/home/jovyan/data/raw"
    output_path = "/home/jovyan/data/tmp"

    print("=== DÉBUT DU PIPELINE ETL ===")

    # 2. Lecture des fichiers sources (Extraction)
    print("Lecture des fichiers sources...")
    df_customers_raw = read_csv(spark, raw_path, "customers.csv")
    df_orders_raw = read_csv(spark, raw_path, "orders.csv")
    df_order_details_raw = read_csv(spark, raw_path, "order_details.csv")

    # 3. Application des transformations (Transformation)
    print("Application des transformations...")
    df_customers_clean = clean_customers(df_customers_raw)
    df_orders_clean = clean_orders(df_orders_raw)
    
    # Nettoyage des détails et ajout du calcul du sous-total
    df_order_details_clean = clean_order_details(df_order_details_raw)
    df_order_details_final = add_sous_total(df_order_details_clean)

    # 4. Écriture des résultats (Chargement / Load)
    print(f"Écriture des données transformées vers {output_path}...")
    write_parquet(df_customers_clean, f"{output_path}/customers")
    write_parquet(df_orders_clean, f"{output_path}/orders")
    write_parquet(df_order_details_final, f"{output_path}/order_details")

    print("=== PIPELINE EXÉCUTÉ AVEC SUCCÈS ===")
    
    # Arrêt propre de la session Spark
    spark.stop()
if __name__ == "__main__":
    main()