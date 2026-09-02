import logging
import sys
from pyspark.sql import SparkSession
from reader import load_raw_data_to_spark
from transformer import build_enriched
from enrichment import enrich_with_currency
from writer import write_clean_data_to_azure

# Configuration du logging structuré et horodaté
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("TradeCorpPipeline")


def run_pipeline():
    """Orchestre le pipeline ETL TradeCorp de bout en bout."""
    logger.info("=== Démarrage du pipeline ETL TradeCorp ===")
    
    # 1. Initialisation de la SparkSession
    spark = SparkSession.builder \
        .appName("TradeCorpPipelineExecution") \
        .getOrCreate()
    
    try:
        # 2. Étape de lecture (Reader) : Téléchargement et chargement des CSV/JSON bruts et de référence
        logger.info("--- ÉTAPE 1 : Lecture des données brutes et de référence ---")
        dfs = load_raw_data_to_spark(spark)
        
        # 3. Étape de transformation (Transformer) : Nettoyage et jointures des tables métier
        logger.info("--- ÉTAPE 2 : Transformation et construction du modèle enrichi ---")
        df_enriched = build_enriched(dfs)
        
        # 4. Étape d'enrichissement (Enrichment) : Ajout de la devise et du sous_total_local
        logger.info("--- ÉTAPE 3 : Enrichissement des devises (sous_total_local) ---")
        df_final = enrich_with_currency(df_enriched, dfs)
        
        # 5. Étape d'écriture (Writer) : Export en Parquet local puis téléversement dans le conteneur clean
        logger.info("--- ÉTAPE 4 : Écriture vers la zone clean d'ADLS Gen2 ---")
        write_clean_data_to_azure(df_final, container_name="clean", dataset_name="tradecorp_enriched")
        
        logger.info("=== Pipeline exécuté avec succès ! ===")
        
    except Exception as e:
        logger.error(f"Erreur critique lors de l'exécution du pipeline : {e}", exc_info=True)
        raise
        
    finally:
        # Arrêt propre de Spark garanti
        logger.info("Arrêt propre de la session Spark.")
        spark.stop()


if __name__ == "__main__":
    run_pipeline()