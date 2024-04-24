from collections import defaultdict, deque
from itertools import combinations
from kafka import KafkaConsumer
import json
import statistics
from pymongo import MongoClient

def initialize_kafka_consumer(topic, servers):
    return KafkaConsumer(topic, bootstrap_servers=servers,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

def initialize_mongodb(uri, db_name, collection_name):
    client = MongoClient(uri)
    db = client[db_name]
    return db[collection_name]

def update_itemsets_and_counts(items, itemsets, item_counts):
    for pair in combinations(items, 2):
        itemsets[frozenset(pair)] += 1
    for item in items:
        item_counts[item] += 1

def detect_anomalies(item_counts, historical_counts, threshold, current_transaction):
    for item, counts in historical_counts.items():
        if len(counts) > 1:
            mean_count = statistics.mean(counts)
            std_dev = statistics.stdev(counts)
            z_score = (item_counts[item] - mean_count) / std_dev
            if abs(z_score) > threshold:
                return {
                    "item": item,
                    "z_score": z_score,
                    "transaction_count": current_transaction
                }

def process_transactions(transactions, window_size, min_support, z_score_threshold, anomalies_collection):
    transaction_count = 0
    frequent_itemsets = defaultdict(int)
    item_counts = defaultdict(int)
    historical_item_counts = defaultdict(list)

    for transaction in transactions:
        transaction_count += 1
        also_buy_items = transaction.get('also_buy', [])
        also_view_items = transaction.get('also_view', [])
        all_items = also_buy_items + also_view_items
        update_itemsets_and_counts(all_items, frequent_itemsets, item_counts)

        for item in all_items:
            historical_item_counts[item].append(item_counts[item])
        
        if transaction_count > window_size:
            anomaly = detect_anomalies(item_counts, historical_item_counts, z_score_threshold, transaction_count)
            if anomaly:
                print(f"Anomaly Detected: Item {anomaly['item']} has a Z-score of {anomaly['z_score']:.2f} at transaction {anomaly['transaction_count']}")
                anomalies_collection.insert_one(anomaly)

def main():
    topic_name = 'processed'
    bootstrap_servers = 'localhost:9092'
    mongo_uri = 'mongodb://localhost:27017/'
    mongo_db_name = 'amazonDB'
    mongo_collection_name = 'anomalies'
    window_size = 1000
    min_support = 0.02
    z_score_threshold = 1.5

    consumer = initialize_kafka_consumer(topic_name, bootstrap_servers)
    anomalies_collection = initialize_mongodb(mongo_uri, mongo_db_name, mongo_collection_name)

    sliding_window = deque(maxlen=window_size)
    for message in consumer:
        sliding_window.append(message.value)
    
    process_transactions(sliding_window, window_size, min_support, z_score_threshold, anomalies_collection)

if __name__ == '__main__':
    main()

