from pyspark.sql import DataFrame
from utils import (
    clean_customers,
    clean_orders,
    clean_order_details,
    add_sous_total,
    clean_employees,
    clean_products
)


def build_enriched(dataframes: dict) -> DataFrame:
    """Nettoie les tables individuelles et les joint pour construire le DataFrame final enrichi."""
    
    # 1. Nettoyage individuel via les fonctions de utils.py
    df_customers = clean_customers(dataframes["customers"])
    df_orders = clean_orders(dataframes["orders"])
    
    # Pour les lignes de commande, on nettoie et on ajoute le sous-total
    df_order_details = clean_order_details(dataframes["order_details"])
    df_order_details = add_sous_total(df_order_details)
    
    df_employees = clean_employees(dataframes["employees"])
    df_products = clean_products(dataframes["products"])
    
    # Catégories et transporteurs pris tels quels selon la consigne
    df_categories = dataframes["categories"]
    df_shippers = dataframes["shippers"]
    
    # 2. Ajout du nom de la catégorie au produit
    # On renomme éventuellement pour éviter les conflits d'ID de catégorie si besoin
    df_products_enriched = df_products.join(
        df_categories.select("category_id", "category_name"),
        on="category_id",
        how="left"
    )
    
    # 3. Jointure des 7 tables en partant de la table de faits (order_details)
    df_enriched = (
        df_order_details
        .join(df_orders, on="order_id", how="inner")
        .join(df_customers, on="customer_id", how="left")
        .join(df_products_enriched, on="product_id", how="left")
        .join(df_employees, on="employee_id", how="left")
        .join(df_shippers, on="shipper_id", how="left")
    )
    
    # 4. Sélection et renommage des colonnes pour correspondre exactement au schéma cible
    df_final = df_enriched.select(
        df_order_details["order_id"],
        df_orders["customer_id"],
        df_orders["employee_id"],  # <-- Un seul employee_id, provenant de orders
        df_order_details["product_id"],
        df_orders["order_date"],
        df_orders["required_date"],
        df_orders["shipped_date"],
        df_orders["freight"],
        df_orders["is_shipped"],
        df_order_details["prix_unitaire"],
        df_order_details["quantite"],
        df_order_details["discount"],
        df_order_details["sous_total"],
        df_customers["company_name"].alias("customer_name"),
        df_customers["country"].alias("customer_country"),
        df_customers["city"].alias("customer_city"),
        df_products_enriched["product_name"],
        df_products_enriched["category_name"],
        df_products_enriched["en_stock"],
        df_employees["full_name"],
        df_shippers["company_name"].alias("shipper_name")
    )
    
    return df_final


if __name__ == "__main__":
    # Test local ou dans le conteneur du transformateur
    from pyspark.sql import SparkSession
    from reader import load_raw_data_to_spark

    spark = SparkSession.builder \
        .appName("TradeCorpTransformerTest") \
        .getOrCreate()

    print("Chargement des données brutes...")
    dfs = load_raw_data_to_spark(spark)
    
    print("Construction du DataFrame enrichi...")
    df_enriched = build_enriched(dfs)
    
    print(f"Schéma final attendu :")
    df_enriched.printSchema()
    
    print(f"Aperçu des premières lignes ({df_enriched.count()} lignes au total) :")
    df_enriched.show(5, truncate=False)