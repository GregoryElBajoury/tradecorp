from datetime import date
from src.transformer import clean_orders


def test_clean_orders(spark):
  """Vérifie que clean_orders supprime bien les lignes où shipped_date est null."""

  # Données de test incluant toutes les colonnes attendues (order_id, order_date, shipped_date, required_date, freight)
  data = [
      (1, date(2026, 1, 1), date(2026, 1, 5), date(2026, 1, 3), 10.5),
      (2, date(2026, 1, 2), None, date(2026, 1, 4), 20.0),
  ]
  columns = [
      "order_id",
      "order_date",
      "shipped_date",
      "required_date",
      "freight",
  ]

  # Création du DataFrame de test via la fixture spark
  df_test = spark.createDataFrame(data, columns)

  # Application de la fonction à tester
  df_result = clean_orders(df_test)
  results = df_result.collect()

  # Assertions : il ne doit rester que la ligne 1
  assert len(results) == 1
  assert results[0]["order_id"] == 1