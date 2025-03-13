import json
import duckdb
from confluent_kafka import Consumer, KafkaException

# Definir o caminho do banco de dados
db_path = "/app/desafios.duckdb"

# Configuração do Kafka
kafka_config = {
    "bootstrap.servers": "kafka:9092",  # Conexão no Docker
    "group.id": "iot_consumer_group",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(kafka_config)
topic = "iot_sensors"

# Conectar ao DuckDB e criar tabela
db_connection = duckdb.connect(db_path)
db_connection.execute("CREATE SCHEMA IF NOT EXISTS sensor_monitor")

db_connection.execute("""
    CREATE TABLE IF NOT EXISTS sensor_monitor.b_sensores_iot (
        sensor_id INTEGER,
        temperature FLOAT,
        humidity FLOAT,
        pressure FLOAT,
        location TEXT,
        timestamp FLOAT
    )
""")

# Função para consumir mensagens e salvar no banco
def consume_messages():
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)  # Aguarda mensagens
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue
                else:
                    print(f"Erro no Kafka: {msg.error()}")
                    break

            # Processa os dados recebidos
            data = json.loads(msg.value().decode("utf-8"))
            print(f"Received: {data}")

            # Insere no banco de dados
            db_connection.execute("""
                INSERT INTO sensor_monitor.b_sensores_iot VALUES (?, ?, ?, ?, ?, ?)
            """, (data["sensor_id"], data["temperature"], data["humidity"],
                  data["pressure"], data["location"], data["timestamp"]))

    except KeyboardInterrupt:
        print("Finalizando consumidor...")
    finally:
        consumer.close()
        db_connection.close()

if __name__ == "__main__":
    consume_messages()