from pyspark.sql import DataFrame, SparkSession

def read_csv(spark: SparkSession, path: str, filename: str) -> DataFrame:
    """Lit un fichier CSV et retourne un DataFrame PySpark."""
    return spark.read.csv(f"{path}/{filename}", header=True, inferSchema=True)