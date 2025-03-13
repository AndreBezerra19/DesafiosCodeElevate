import json
import time
import random
from confluent_kafka import Producer
from faker import Faker

# Faker init
fake = Faker()

# Kafka configs
conf = {
    'bootstrap.servers': 'kafka:9092',  # Alterando de localhost para kafka
    'client.id': 'sensor-producer'
}

producer = Producer(conf)
topic = "iot_sensors"

# gerar dados
def generate_sensor_data():
    sensor_id = random.randint(1, 20)
    temperature = round(random.uniform(0.0, 40.0), 2)
    humidity = round(random.uniform(20.0, 80.0), 2)
    pressure = round(random.uniform(900, 1100), 2)
    location = fake.city() 
    
    data = {
        "sensor_id": sensor_id,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "location": location,
        "timestamp": time.time()
    }
    
    return json.dumps(data)

# enviar dados para o kafka
def send_to_kafka():
    while True:
        message = generate_sensor_data()
        producer.produce(topic, key=str(random.randint(1, 100)), value=message)
        producer.flush()
        print(f"Sent: {message}")
        time.sleep(5)  # intervale entre as leituras

if __name__ == "__main__":
    send_to_kafka()
