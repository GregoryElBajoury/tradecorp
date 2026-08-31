import pytest
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

@pytest.fixture(scope="session")
def spark():
    conf = SparkConf().setAppName("TradeCorp-TestSuite").setMaster("local[2]")
    sc = SparkContext.getOrCreate(conf=conf)
    spark_session = SparkSession(sc)
    
    yield spark_session
    
    spark_session.stop()