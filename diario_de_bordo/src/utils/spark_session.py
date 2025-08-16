from pyspark.sql import SparkSession

def get_spark_session(app_name: str) -> SparkSession:
    """Cria e retorna uma sessão Spark configurada para Iceberg."""
    return (
        SparkSession.builder
        .appName(app_name)
        .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.spark_catalog.type", "hadoop")
        .config("spark.sql.catalog.spark_catalog.warehouse", "../data/warehouse")
        .getOrCreate()
    )