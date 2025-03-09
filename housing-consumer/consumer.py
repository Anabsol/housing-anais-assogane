from confluent_kafka import Consumer
import requests
import json

KAFKA_TOPIC = "housing_topic"
KAFKA_BROKER = "broker:9092"
API_ENDPOINT = "http://housing-api:8000/houses"
MODEL_ENDPOINT = "http://127.0.0.1:8080/invocations"

consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'housing-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subscribe([KAFKA_TOPIC])

print("Consumer started. Waiting for messages...")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue
    
    house_data = json.loads(msg.value().decode('utf-8'))
    print(f"Received message: {house_data}")

    # Prepare data for ML model
    model_payload = {
        "dataframe_split": {
            "columns": [
                "longitude", "latitude", "housing_median_age", "total_rooms",
                "total_bedrooms", "population", "households", "median_income"
            ],
            "data": [[
                house_data["longitude"], house_data["latitude"], house_data["housing_median_age"],
                house_data["total_rooms"], house_data["total_bedrooms"], house_data["population"],
                house_data["households"], house_data["median_income"]
            ]]
        }
    }

    # Get prediction from MLflow model
    model_response = requests.post(MODEL_ENDPOINT, json=model_payload, headers={"Content-Type": "application/json"})
    
    if model_response.status_code == 200:
        prediction = model_response.json()["predictions"][0]
        house_data["estimated_median_house_value"] = prediction
        print(f"Predicted house value: {prediction}")

        # Send data to API
        api_response = requests.post(API_ENDPOINT, json=house_data)
        print(f"API Response: {api_response.status_code}, {api_response.text}")
    else:
        print(f"Model error: {model_response.status_code}, {model_response.text}")
