# Imagem Python
FROM python:3.10

WORKDIR /app

# Dependências
RUN apt-get update && apt-get install -y default-jdk && rm -rf /var/lib/apt/lists/*

# Instalar DuckDB via pip
RUN pip install duckdb

# Definir JAVA_HOME
RUN export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
ENV JAVA_HOME=$JAVA_HOME
ENV PATH="$JAVA_HOME/bin:$PATH"

# Garantir que PySpark use a mesma versão de Python no driver e worker
ENV PYSPARK_PYTHON=python3.10
ENV PYSPARK_DRIVER_PYTHON=python3.10

# Copiar os arquivos do projeto para o container
COPY . /app

# Dependências Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expor portas do Kafka e outras necessárias
EXPOSE 9092 2181

# Definir o comando padrão do container
CMD ["tail", "-f", "/dev/null"]
