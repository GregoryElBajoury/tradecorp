# Notebook 5 — Programmation modulaire et tests unitaires (Jour 4 après-midi + Jour 5)
#💡 On sort des notebooks. Créer des fichiers .py dans le dossier src/. Ces fichiers seront exécutés avec spark-submit depuis le conteneur Docker.
"""
Q44 — Créer test_transformer.py
Créer tests/test_transformer.py. Écrire un test qui vérifie que clean_orders() supprime bien les lignes où
shipped_date est null.
Indice : from pyspark.sql import SparkSession / spark = SparkSession.builder.getOrCreate() / df_test =
spark.createDataFrame(...)
"""
from datetime import date
from transformer import clean_orders

def test_clean_orders(spark):  # <- On injecte la fixture 'spark' ici
    # Une ligne avec une date valide et une ligne avec shipped_date à None (qui doit être supprimée)
    data = [
        (1, date(2026, 1, 1), date(2026, 1, 5)),
        (2, date(2026, 1, 2), None)
    ]
    columns = ["order_id", "order_date", "shipped_date"]
    
    df_test = spark.createDataFrame(data, columns)
    df_result = clean_orders(df_test)

    results = df_result.collect()
    
    # On vérifie qu'il ne reste qu'une seule ligne (celle où shipped_date n'est pas null)
    assert len(results) == 1
    assert results[0]["order_id"] == 1
    print("Test clean_orders validé avec succès !")