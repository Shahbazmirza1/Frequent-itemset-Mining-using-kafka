from kafka import KafkaConsumer
from collections import Counter, defaultdict
import json
import itertools
from pymongo import MongoClient


# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Adjust the connection string as needed
db = client['amazonDB']  # Database where the rules will be stored
collection = db['PCY_rules']  # Collection within the database

association_rule_schema = {
	'antecedent': [],
        'consequent': [],
        'confidence': float,
        'count': int,
        'total_transactions': int
    }

topic = 'processed'

global_item_counter = Counter()
global_pair_counter = Counter()  # Initialize global counter for pairs
buckets = []
bitmap = []

def hash_function(item1, item2, num_buckets):
    return hash(str(item1) + str(item2)) % num_buckets

def apply_decay(counter, decay_factor):
    for item in list(counter.keys()):
        counter[item] *= decay_factor
        if counter[item] < 1:
            del counter[item]
            
            
def generate_association_rules(pair_counts, item_counts, total_transactions, min_confidence=0.75):
    rules = []
    for (item1, item2), pair_support in pair_counts.items():
        support_item1 = item_counts[item1]
        support_item2 = item_counts[item2]

        # Calculate confidence for the rules
        confidence_item1_to_item2 = (pair_support / support_item1) if support_item1 else 0
        confidence_item2_to_item1 = (pair_support / support_item2) if support_item2 else 0

        # Check if the confidence meets the minimum threshold
        if confidence_item1_to_item2 >= min_confidence:
            rules.append({
                'antecedent': [item1],
                'consequent': [item2],
                'confidence': confidence_item1_to_item2,
                'count': pair_support,
                'total_transactions': total_transactions
            })
        if confidence_item2_to_item1 >= min_confidence:
            rules.append({
                'antecedent': [item2],
                'consequent': [item1],
                'confidence': confidence_item2_to_item1,
                'count': pair_support,
                'total_transactions': total_transactions
            })

    return rules

def consume_messages(consumer, min_support, window_size, decay_factor, num_buckets):
    transactions = []
    buckets = [0] * num_buckets
    pair_counts = defaultdict(int)
    total_transactions = 0
    item_counts = defaultdict(int)  # To track counts of individual items

    try:
        for message in consumer:
            data = message.value['also_buy'] + [message.value['asin']]
            transactions.append(data)

            # Update item counts within the transaction
            for item in data:
                item_counts[item] += 1

            if total_transactions % window_size == 0 and total_transactions != 0:
                # Counting pairs and updating buckets
                for transaction in transactions:
                    seen_pairs = set()
                    for item1, item2 in itertools.combinations(sorted(set(transaction)), 2):
                        if (item1, item2) not in seen_pairs:
                            bucket_index = hash_function(item1, item2, num_buckets)
                            buckets[bucket_index] += 1
                            pair_counts[(item1, item2)] += 1
                            global_pair_counter[(item1, item2)] += 1  # Update global pair counter
                            seen_pairs.add((item1, item2))

                # Create bitmap for frequent buckets
                bitmap = [1 if count >= min_support else 0 for count in buckets]

                # Consolidate information and prepare for print
                pairs_to_print = [
                    (pair, pair_counts[pair], hash_function(pair[0], pair[1], num_buckets))
                    for pair in pair_counts
                    if bitmap[hash_function(pair[0], pair[1], num_buckets)] and pair_counts[pair] >= min_support
                ]

                # Print information about pairs
                #for pair, count, bucket_index in pairs_to_print:
                 #   support_percent = (count / total_transactions) * 100
                  #  print(f"Pair: {pair}, Bucket: {bucket_index}, Count: {count}, Support (%): {support_percent:.2f}")

                # Generate and print rules
                rules = generate_association_rules(pair_counts, item_counts, total_transactions)
                if rules:
                	collection.insert_many(rules)
                	for rule, confidence, support in rules:
                    		print(f"Rule: {rule}, Confidence: {confidence:.2f}, Support: {support}/total_transactions")
                    

                # Reset pair counts and item counts after printing to avoid redundancy
                pair_counts.clear()
                item_counts.clear()

                # Apply decay
                apply_decay(global_pair_counter, decay_factor)
                transactions.clear()

            total_transactions += 1

    except KeyboardInterrupt:
        print("Stopped consuming due to user interruption.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        consumer.close()
        print("Kafka Consumer closed successfully.")

if __name__ == "__main__":
    min_support = 290 # Adjusted minimum support threshold for testing
    window_size = 5000  # Manageable window size for processing
    decay_factor = 0.95  # Decay factor to apply to counts
    num_buckets = 1000 # Number of buckets for hashing

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id='batchGroup',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        max_poll_records=200
    )

    print(f"Starting to consume messages from {topic}")
    consume_messages(consumer, min_support, window_size, decay_factor, num_buckets)

