from abc import ABC, abstractmethod
from pyspark.sql import SparkSession

class BasePipeline(ABC):
    def __init__(self, spark: SparkSession):
        self.spark = spark

    @abstractmethod
    def run(self):
        """Método abstrato para execução do pipeline."""
        pass