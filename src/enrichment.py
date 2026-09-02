from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, MapType, StringType


def enrich_with_currency(df_enriched: DataFrame, dfs: dict) -> DataFrame:
  """Détermine la devise de chaque client et convertit le sous_total en sous_total_local."""
  df_country_currency = dfs["country_currency"]

  # 1. Préparation du mapping pays -> devise
  df_cc = df_country_currency.select(
      F.col("country").alias("cc_country"),
      F.col("currency").alias("currency_code"),
  )

  # 2. Jointure pour associer chaque ligne au code devise du client
  df_with_currency = df_enriched.join(
      df_cc, df_enriched["customer_country"] == df_cc["cc_country"], how="left"
  ).drop("cc_country")

  # 3. Gestion des taux : soit c'est un dictionnaire direct (pour les tests), soit c'est le DataFrame d'origine
  exchange_rates_input = dfs.get("exchange_rates")

  if isinstance(exchange_rates_input, dict):
    # Si c'est un dictionnaire Python direct (cas du test unitaire)
    rates_data = [(k, float(v)) for k, v in exchange_rates_input.items()]
    df_rates_map = spark_session_from_df = (  # ou création directe via spark actif
        df_enriched.sparkSession.createDataFrame(
            rates_data, ["rate_currency", "rate_value"]
        )
    )
  else:
    # Cas nominal (pipeline avec le DataFrame Spark et son struct rates)
    df_rates_map = exchange_rates_input.select(
        F.explode(
            F.from_json(
                F.to_json(F.col("rates")), "MAP<STRING, DOUBLE>"
            )
        ).alias("rate_currency", "rate_value")
    )

  # 4. Jointure avec les taux de change éclatés
  df_with_rate = df_with_currency.join(
      df_rates_map,
      df_with_currency["currency_code"] == df_rates_map["rate_currency"],
      how="left",
  )

  # 5. Calcul de sous_total_local
  df_final_enriched = df_with_rate.withColumn(
      "sous_total_local",
      F.col("sous_total") * F.coalesce(F.col("rate_value"), F.lit(1.0)),
  ).drop("rate_currency", "rate_value")

  return df_final_enriched