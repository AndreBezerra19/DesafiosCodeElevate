from src.utils.spark_session import get_spark_session
from src.utils.logger import setup_logger
from src.pipeline.bronze_pipeline import BronzePipeline
from src.config import RAW_DATA_PATH, BRONZE_TABLE

def main():
    # Configurar logger
    logger = setup_logger()
    logger.info("Iniciando o pipeline...")

    # Criar sessão Spark
    spark = get_spark_session("DiarioDeBordoPipeline")

    # Executar pipeline Bronze
    logger.info("Executando pipeline Bronze...")
    bronze_pipeline = BronzePipeline(spark, RAW_DATA_PATH, BRONZE_TABLE)
    bronze_pipeline.run()

    logger.info("Pipeline concluído.")

if __name__ == "__main__":
    main()