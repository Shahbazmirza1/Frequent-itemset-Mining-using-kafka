from kafka import KafkaConsumer
import json
import re
from pymongo import MongoClient

bootstrap_servers = ['localhost:9092']
topic = 'amazon_data' 

# Setup MongoDB connection
client = MongoClient('localhost', 27017)  # Default MongoDB port is 27017
db = client['amazonDB']  # Create a new database 
collection = db['products']  # Create a new collection 

def store_in_mongodb(data):
    try:
        # Use 'asin' as the document ID in MongoDB
        data['_id'] = data['asin']
        # Insert data into MongoDB, handling duplicates
        result = collection.replace_one({'_id': data['_id']}, data, upsert=True)
        print(f"Data inserted/updated for ASIN: {data['asin']}")
    except Exception as e:
        print(f"An error occurred while inserting data into MongoDB: {e}")



def remove_html_tags(text):
    """Remove html tags and JavaScript from a string"""
    text = re.sub('<script.*?</script>', '', text, flags=re.DOTALL)  # Remove JavaScript
    text = re.sub('<style.*?</style>', '', text, flags=re.DOTALL)  # Remove style content
    clean_text = re.sub('<.*?>', '', text)  # Remove remaining HTML tags
    return re.sub('\s+', ' ', clean_text).strip()  # Remove extra spaces and strip


def preprocess_data(data):
    remove = ["description", "price", "imageURL", "imageURLHighRes", "salesRank", "tech1", "tech2", "categories",'details','image','Average Customer Review','fit','rank','date','similar_item','category']
    
    # Remove specified columns from the data
    for column in remove:
        data.pop(column, None)

    # Remove HTML from all string fields
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = remove_html_tags(value)
        elif isinstance(value, list):
            data[key] = [remove_html_tags(item) if isinstance(item, str) else item for item in value]

    return data


def consume_messages(consumer):
    try:
        while True:
            batch = consumer.poll(timeout_ms=1000)  
            if batch:
                for tp, messages in batch.items():
                    for message in messages:
                        data = preprocess_data(message.value)
                        print("Received message:")
                        print(f"Topic: {tp.topic}")
                        print("Value:")
                        for key, value in data.items():
                            if isinstance(value, list) and len(value) > 10:
                                print(f"  {key}: [{', '.join(value[:10])}... +{len(value)-10} more]")
                            else:
                                print(f"  {key}: {value}")
                        # Store the processed data into MongoDB
                        store_in_mongodb(data)
                        print("-" * 50)
                consumer.commit() 
    except KeyboardInterrupt:
        print("Stopped consuming due to user interruption.")
    finally:
        consumer.close()
        print("Kafka Consumer closed successfully.")




if __name__ == "__main__":
    consumer = KafkaConsumer(topic, 		bootstrap_servers=bootstrap_servers,auto_offset_reset='earliest',enable_auto_commit=False,group_id='batchGroup',value_deserializer=lambda x: json.loads(x.decode('utf-8')),max_poll_records=100 )

    if consumer:
        print(f"Starting to consume messages from {topic}")
        consume_messages(consumer)

