from src.enrichment import enrich_with_currency


def test_add_currency_column(spark):
  """Vérifie l'enrichissement des devises avec un dictionnaire de taux simulé en dur."""
  # 1. Données de test minimales
  orders_data = [(10248, "VINET", "France", 100.0)]
  df_test = spark.createDataFrame(
      orders_data, ["order_id", "customer_id", "customer_country", "sous_total"]
  )

  country_currency_data = [("France", "EUR")]
  df_cc = spark.createDataFrame(
      country_currency_data, ["country", "currency"]
  )

  # 2. Dictionnaire de taux simulé (codé en dur, sans appel réseau)
  mock_exchange_rates = {"EUR": 1.0, "USD": 1.08}

  # 3. Dictionnaire de référence passé à la fonction
  dfs_mock = {"country_currency": df_cc, "exchange_rates": mock_exchange_rates}

  # 4. Application de la fonction
  df_result = enrich_with_currency(df_test, dfs_mock)
  results = df_result.collect()

  # 5. Assertions
  assert "currency_code" in df_result.columns
  assert "sous_total_local" in df_result.columns
  assert results[0]["currency_code"] == "EUR"
  assert results[0]["sous_total_local"] == 100.0