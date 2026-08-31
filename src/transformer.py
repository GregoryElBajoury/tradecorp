# src/transformer.py

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, trim, initcap

def clean_customers(df: DataFrame) -> DataFrame:
    """Applique les transformations sur les clients (trim, initcap, gestion des valeurs nulles)."""
    return df \
        .withColumn("contact_name", initcap(trim(col("contact_name")))) \
        .withColumn("company_name", trim(col("company_name"))) \
        .withColumn("country", initcap(trim(col("country"))) if "country" in df.columns else col("country")) \
        .fillna({"region": "Unknown"})

def clean_orders(df: DataFrame) -> DataFrame:
    """Nettoie les commandes (typage des dates et filtrage des lignes corrompues si besoin)."""
    return df \
        .withColumn("order_date", col("order_date").cast("date")) \
        .withColumn("shipped_date", col("shipped_date").cast("date")) \
        .filter(col("shipped_date").isNotNull())

def clean_order_details(df: DataFrame) -> DataFrame:
    """Nettoie les détails de commandes (typage des numériques)."""
    return df \
        .withColumn("unit_price", col("unit_price").cast("float")) \
        .withColumn("quantity", col("quantity").cast("integer")) \
        .withColumn("discount", col("discount").cast("float"))

def add_sous_total(df: DataFrame) -> DataFrame:
    """Calcule et ajoute la colonne sous_total."""
    return df.withColumn(
        "sous_total",
        col("unit_price") * col("quantity") * (1 - col("discount"))
    )