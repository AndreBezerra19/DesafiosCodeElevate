import unittest
from pyspark.sql import SparkSession
from src.pipeline.bronze_pipeline import BronzePipeline

class TestBronzePipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura a sessão Spark para os testes."""
        cls.spark = SparkSession.builder \
            .appName("TestBronzePipeline") \
            .master("local[*]") \
            .getOrCreate()

    @classmethod
    def tearDownClass(cls):
        """Finaliza a sessão Spark após os testes."""
        cls.spark.stop()

    def setUp(self):
        """Configura os dados simulados para os testes."""
        self.raw_data_path = "tests/resources/raw_data.csv"
        self.bronze_table = "tests_bronze_table"
        self.pipeline = BronzePipeline(self.spark, self.raw_data_path, self.bronze_table)

        # Dados simulados
        self.sample_data = [
            ("01-01-2016 21:11", "01-01-2016 21:17", "Negocio", "Fort Pierce", "Fort Pierce", 51, "Alimentação"),
            ("01-02-2016 01:25", "01-02-2016 01:37", "Negocio", "Fort Pierce", "Fort Pierce", 5, None),
        ]
        self.sample_schema = ["DATA_INICIO", "DATA_FIM", "CATEGORIA", "LOCAL_INICIO", "LOCAL_FIM", "DISTANCIA", "PROPOSITO"]

    def test_read_raw_data(self):
        """Testa se os dados brutos são lidos corretamente."""
        # Criar um DataFrame de teste
        df = self.spark.createDataFrame(self.sample_data, schema=self.sample_schema)
        df.write.csv(self.raw_data_path, header=True, mode="overwrite")

        # Ler os dados usando o pipeline
        result_df = self.pipeline.read_raw_data()

        # Verificar se os dados lidos são iguais aos esperados
        self.assertEqual(result_df.count(), len(self.sample_data))
        self.assertEqual(len(result_df.columns), len(self.sample_schema))

    def test_write_to_bronze(self):
        """Testa se os dados são escritos corretamente na camada Bronze."""
        # Criar um DataFrame de teste
        df = self.spark.createDataFrame(self.sample_data, schema=self.sample_schema)

        # Escrever os dados na tabela Bronze
        self.pipeline.write_to_bronze(df)

        # Ler os dados da tabela Bronze
        result_df = self.spark.read.table(self.bronze_table)

        # Verificar se os dados escritos são iguais aos esperados
        self.assertEqual(result_df.count(), len(self.sample_data))
        self.assertEqual(len(result_df.columns), len(self.sample_schema))

if __name__ == "__main__":
    unittest.main()