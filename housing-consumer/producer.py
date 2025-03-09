from confluent_kafka import Producer
import json
import time

KAFKA_TOPIC = "housing_topic"
KAFKA_BROKER = "localhost:29092"

producer_conf = {
    'bootstrap.servers': KAFKA_BROKER
}

producer = Producer(producer_conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

sample_message = {
    "longitude": -122.23,
    "latitude": 37.88,
    "housing_median_age": 52,
    "total_rooms": 880,
    "total_bedrooms": 129,
    "population": 322,
    "households": 126,
    "median_income": 8.3252,
    "median_house_value": 358500,
    "ocean_proximity": "NEAR BAY"
}

while True:
    producer.produce(KAFKA_TOPIC, json.dumps(sample_message).encode('utf-8'), callback=delivery_report)
    producer.flush()
    time.sleep(5)
