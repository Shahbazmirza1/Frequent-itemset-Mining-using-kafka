import json
from kafka import KafkaProducer
from kafka.errors import KafkaError

def send_data(producer, topic, data):
    try:
        future = producer.send(topic, value=data)
        # Block for 'synchronous' sends to ensure data integrity
        result = future.get(timeout=10)
        print("Data sent to Kafka topic:", data)
    except KafkaError as e:
        print("Failed to send data to Kafka:", str(e))
    except Exception as e:
        print("An error occurred:", str(e))

def read(path, topic):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    try:
        with open(path, 'r') as file:
            for line in file:
                data = json.loads(line.strip())
                send_data(producer, topic, data)
    except FileNotFoundError:
        print("JSON file not found:", path)
    finally:
        if producer:
            producer.flush()
            producer.close()
            print("Kafka Producer closed successfully.")

if __name__ == "__main__":
    path = '/home/shahbaz/Downloads/sample_data.json'
    topic = 'amazon_data'
    read(path,topic)

