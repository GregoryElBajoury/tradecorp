from pyspark.sql import DataFrame

def write_parquet(df: DataFrame, path: str) -> None:
    """
    Écrit un DataFrame PySpark au format Parquet à l'emplacement spécifié.
    Utilise le mode 'overwrite' pour remplacer les données existantes.
    """
    df.write \
        .mode("overwrite") \
        .parquet(path)

def write_postgres(df: DataFrame, table_name: str, jdbc_url: str, properties: dict) -> None:
    """
    Écrit un DataFrame PySpark dans une table PostgreSQL via une connexion JDBC.
    Utilise le mode 'append' ou 'overwrite' selon le besoin (par défaut 'append' ou 'overwrite').
    """
    df.write \
        .jdbc(url=jdbc_url, table=table_name, mode="overwrite", properties=properties)