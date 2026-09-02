import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, initcap, lit, lower, round, trim, upper, when
from pyspark.sql.types import DateType, DoubleType, IntegerType

load_dotenv()

# --- CONNEXION ET GESTION ADLS GEN2 ---

def get_blob_service_client() -> BlobServiceClient:
    """Initialise et retourne le client Blob Service pour Azure ADLS Gen2."""
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
    connect_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    return BlobServiceClient.from_connection_string(connect_str)


def download_blob_to_local(blob_service_client: BlobServiceClient, container_name: str, blob_name: str, download_path: str):
    """Télécharge un fichier spécifique depuis un conteneur ADLS Gen2 vers le système local."""
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    os.makedirs(os.path.dirname(download_path), exist_ok=True)
    with open(download_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())


# --- FONCTIONS DE NETTOYAGE PAR TABLE ---

def clean_customers(df: DataFrame) -> DataFrame:
    """Nettoie la table des clients : trim, normalisation et déduplication."""
    return (
        df.withColumn("company_name", trim(col("company_name")))
          .withColumn("contact_name", initcap(trim(col("contact_name"))))
          .withColumn("country", upper(trim(col("country"))))
          .dropDuplicates(["customer_id"])
    )


def clean_orders(df: DataFrame) -> DataFrame:
    """Nettoie la table des commandes : filtrage des non-livrées, retypage et renommage."""
    return (
        df.filter(col("shipped_date").isNotNull())
          .withColumn("order_date", col("order_date").cast(DateType()))
          .withColumn("required_date", col("required_date").cast(DateType()))
          .withColumn("shipped_date", col("shipped_date").cast(DateType()))
          .withColumn("freight", col("freight").cast(DoubleType()))
          .withColumnRenamed("ship_via", "shipper_id")
          .withColumn("is_shipped", when(col("shipped_date").isNotNull(), True).otherwise(False))
    )


def clean_order_details(df: DataFrame) -> DataFrame:
    """Nettoie le détail des lignes de commande et renomme les colonnes en français."""
    return (
        df.withColumn("unit_price", col("unit_price").cast(DoubleType()))
          .withColumn("quantity", col("quantity").cast(IntegerType()))
          .withColumn("discount", col("discount").cast(DoubleType()))
          .withColumnRenamed("unit_price", "prix_unitaire")
          .withColumnRenamed("quantity", "quantite")
    )


def add_sous_total(df: DataFrame) -> DataFrame:
    """Calcule le sous-total d'une ligne de commande (prix × quantité × (1 - remise))."""
    return df.withColumn(
        "sous_total",
        round(col("prix_unitaire") * col("quantite") * (lit(1) - col("discount")), 2)
    )


def clean_employees(df: DataFrame) -> DataFrame:
    """Filtre les colonnes utiles des employés et crée full_name."""
    cols_to_keep = ["employee_id", "first_name", "last_name", "title", "hire_date", "city", "country"]
    return (
        df.select([c for c in cols_to_keep if c in df.columns])
          .withColumn("full_name", trim(col("first_name")) + lit(" ") + trim(col("last_name")))
    )


def clean_products(df: DataFrame) -> DataFrame:
    """Nettoie la table des produits, convertit le prix et ajoute l'indicateur de stock."""
    return (
        df.withColumn("unit_price", col("unit_price").cast(DoubleType()))
          .withColumn("en_stock", when(col("units_in_stock") > 0, True).otherwise(False))
    )

# Verification
print(f"Compte de stockage : {os.getenv('AZURE_STORAGE_ACCOUNT_NAME')}")
print(f"Clé de stockage présente : {bool(os.getenv('AZURE_STORAGE_ACCOUNT_KEY'))}")

