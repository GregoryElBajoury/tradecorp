# Notebook 5 — Programmation modulaire et tests unitaires (Jour 4 après-midi + Jour 5)
#💡 On sort des notebooks. Créer des fichiers .py dans le dossier src/. Ces fichiers seront exécutés avec spark-submit depuis le conteneur Docker.

"""
Q46 — Test sur clean_customers
Écrire un test qui vérifie que clean_customers() applique bien le trim et l'initcap sur contact_name.

"""
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from transformer import clean_customers

def test_clean_customers(spark):  # <- On injecte la fixture 'spark' ici
    # Définition explicite du schéma pour éviter les erreurs de type
    schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("contact_name", StringType(), True),
        StructField("company_name", StringType(), True),
        StructField("country", StringType(), True),
        StructField("region", StringType(), True)
    ])

    data = [(1, "  jean dupont  ", "  trade corp  ", "france", "North")]
    
    df_test = spark.createDataFrame(data, schema)
    df_result = clean_customers(df_test)

    results = df_result.collect()
    assert len(results) == 1
    assert results[0]["contact_name"] == "Jean Dupont"
    print("Test clean_customers validé avec succès !")