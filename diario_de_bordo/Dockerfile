# Imagem base - Spark e Hadoop 
FROM bitnami/spark:4.0.0

# Trocar para o usuário root para executar comandos com permissões elevadas
USER root

# Corrigir o problema do apt-get update e instalar Miniconda para ARM64
RUN mkdir -p /var/lib/apt/lists/partial && apt-get update && apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh && \
    /opt/conda/bin/conda init bash

# Retornar ao usuário padrão para segurança
USER 1001

# Conda PATH
ENV PATH="/opt/conda/bin:$PATH"

# Configurar o cache do Conda e o diretório de ambientes
ENV CONDA_PKGS_DIRS=/opt/conda/pkgs
ENV CONDA_ENVS_PATH=/opt/conda/envs
RUN mkdir -p /opt/conda/pkgs /opt/conda/envs

# Dependências Conda
COPY environment.yml /app/environment.yml

# Instalar dependências do Conda
RUN conda env create -f /app/environment.yml

# Ativar ambiente Conda
SHELL ["conda", "run", "-n", "diario_de_bordo", "/bin/bash", "-c"]

# Configura o Iceberg (baixa o JAR)
RUN mkdir -p /app/jars && \
    wget https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-4.0/iceberg-spark-runtime-4.0.jar -P /app/jars

# Diretório de trabalho
WORKDIR /app

# Código do projeto
COPY . /app

# Configura o Spark para Iceberg
ENV SPARK_JARS="/app/jars/iceberg-spark-runtime-4.0.jar"

# Rodar o pipeline
CMD ["python", "src/main.py"]