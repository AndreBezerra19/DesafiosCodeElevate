import json
import time
import random
from confluent_kafka import Producer
from faker import Faker

# Faker init
fake = Faker()

# Kafka configs
kafka_config = {
    "bootstrap.servers": "localhost:9092"  # Ajuste conforme necessário
}

producer = Producer(kafka_config)
topic = "iot_sensors"

# data generation function
def generate_sensor_data():
    sensor_id = random.randint(1, 20)
    temperature = round(random.uniform(0.0, 40.0), 2)
    humidity = round(random.uniform(20.0, 80.0), 2)
    pressure = round(random.uniform(900, 1100), 2)
    location = fake.city()  # make random city
    
    data = {
        "sensor_id": sensor_id,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "location": location,
        "timestamp": time.time()
    }
    
    return json.dumps(data)

# send data function
def send_to_kafka():
    while True:
        message = generate_sensor_data()
        producer.produce(topic, key=str(random.randint(1, 100)), value=message)
        producer.flush()
        print(f"Sent: {message}")
        time.sleep(5)  # creates a gap between sensor readings

if __name__ == "__main__":
    send_to_kafka()