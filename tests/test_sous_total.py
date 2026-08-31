# Notebook 5 — Programmation modulaire et tests unitaires (Jour 4 après-midi + Jour 5)
#💡 On sort des notebooks. Créer des fichiers .py dans le dossier src/. Ces fichiers seront exécutés avec spark-submit depuis le conteneur Docker.

"""
Q45 — Test sur sous_total
Écrire un test qui vérifie que add_sous_total() calcule correctement le sous_total. Créer un petit DataFrame de
test avec des valeurs connues et vérifier le résultat.
Indice : Valeur attendue : 10.0 * 2 * (1 - 0.1) = 18.0

"""
from transformer import add_sous_total

def test_add_sous_total(spark):  # <- On injecte la fixture 'spark' ici
    # Données de test basées sur l'indice : 10.0 * 2 * (1 - 0.1) = 18.0
    data = [(10.0, 2, 0.1)]
    columns = ["unit_price", "quantity", "discount"]
    
    df_test = spark.createDataFrame(data, columns)
    df_result = add_sous_total(df_test)

    results = df_result.collect()
    assert len(results) == 1
    # On suppose que la colonne calculée s'appelle "sous_total"
    assert results[0]["sous_total"] == 18.0
    print("Test add_sous_total validé avec succès !")