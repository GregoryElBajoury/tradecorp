
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="function")
def spark():
    # Arrête proprement toute session active précédente pour éviter les conflits JVM
    if SparkSession.getActiveSession():
        SparkSession.getActiveSession().stop()
        
    spark_session = (
        SparkSession.builder
        .appName("TradeCorp-TestSuite")
        .master("local[2]")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    
    yield spark_session
    
    # Nettoyage après le test
    spark_session.stop()