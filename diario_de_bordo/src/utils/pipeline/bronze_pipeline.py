from pyspark.sql import DataFrame
from src.pipeline.base_pipeline import BasePipeline

class BronzePipeline(BasePipeline):
    def __init__(self, spark, raw_data_path: str, bronze_table: str):
        super().__init__(spark)
        self.raw_data_path = raw_data_path
        self.bronze_table = bronze_table

    def read_raw_data(self) -> DataFrame:
        """Lê os dados brutos do CSV."""
        return self.spark.read.csv(self.raw_data_path, header=True, sep=";")

    def write_to_bronze(self, df: DataFrame):
        """Escreve os dados na tabela Bronze."""
        df.writeTo(self.bronze_table).createOrReplace()

    def run(self):
        """Executa o pipeline da camada Bronze."""
        raw_df = self.read_raw_data()
        self.write_to_bronze(raw_df)