from utils import clean_customers
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

def test_clean_customers(spark):
    """Vérifie que clean_customers() applique trim, initcap sur contact_name et upper sur country."""
    schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("contact_name", StringType(), True),
        StructField("company_name", StringType(), True),
        StructField("country", StringType(), True),
        StructField("region", StringType(), True)
    ])

    # On ajoute un doublon pour tester aussi la déduplication
    data = [
        (1, "  jean dupont  ", "  trade corp  ", "france", "North"),
        (1, "  jean dupont  ", "  trade corp  ", "france", "North")
    ]
    
    df_test = spark.createDataFrame(data, schema)
    df_result = clean_customers(df_test)

    results = df_result.collect()
    
    # Vérifications
    assert len(results) == 1  # Test de la déduplication
    assert results[0]["contact_name"] == "Jean Dupont"
    assert results[0]["country"] == "FRANCE"
    print("Test clean_customers validé avec succès !")