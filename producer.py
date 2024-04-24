from pymongo import MongoClient
from kafka import KafkaProducer
import json

client = MongoClient('localhost', 27017)
db = client['amazonDB']
collection = db['products']

topic = 'processed'

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def publish():
    cursor = collection.find()  # Adjust the query as needed
    for record in cursor:
        data = {
            "title": record.get("title", ""),
            "also_buy": record.get("also_buy", []),
            "brand": record.get("brand", ""),
            "feature": record.get("feature", []),
            "also_view": record.get("also_view", []),
            "main_cat": record.get("main_cat", ""),
            "asin": record.get("asin", "")
        }
        print(f"ASIN: {data['asin']}")
        print(f"Title: {data['title']}")
        print(f"Brand: {data['brand']}")
        print(f"Main Category: {data['main_cat']}")
        print(f"Also Bought: {data['also_buy']}")
        print(f"Features: {data['feature']}")
        print(f"Also Viewed: {data['also_view']}")
        print("-" * 50)
        # Send data to another Kafka topic
        producer.send(topic, value=data)
    producer.flush()

if __name__ == "__main__":
    publish()

