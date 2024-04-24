from kafka import KafkaConsumer
import json
from itertools import combinations,chain
from collections import Counter, defaultdict
from pymongo import MongoClient

# Kafka setup
topic = 'processed'
bootstrap_servers = ['localhost:9092']

# Setup MongoDB connection
client = MongoClient('localhost', 27017)  # Default MongoDB port is 27017
db = client['amazonDB']  # Create a new database 
collection = db['apriori']  # Create a new collection 
    
    # Define a schema for association rules documents
association_rule_schema = {
	'antecedent': [],
        'consequent': [],
        'confidence': float,
        'count': int,
        'total_transactions': int
    }
    


# Global counters for items and pairs
global_item_counter = Counter()
global_pair_counter = Counter()
global_triplet_counter = Counter()
global_quadruplet_counter = Counter()

#pass1
def C1(transactions, min_support):
    # Local count within this window
    local_item_counter = Counter(item for transaction in transactions for item in transaction)
    global_item_counter.update(local_item_counter)  # Update global counter with local counts

    # Filter for frequent items globally
    frequent_items = {item for item, count in global_item_counter.items() if count >= min_support}
    return frequent_items


#pass2
def C2(transactions, frequent_items, min_support):
    # Filter transactions to only include frequent items
    frequent_items_set = set(frequent_items)

    for transaction in transactions:
        items_in_transaction = set(transaction).intersection(frequent_items_set)
        for pair in combinations(sorted(items_in_transaction), 2):
            global_pair_counter[pair] += 1

    # Filter for frequent pairs globally
    frequent_pairs = {pair for pair, count in global_pair_counter.items() if count >= min_support}
    return frequent_pairs


#pass3
def C3(transactions, frequent_items, frequent_pairs, min_support):
    # Filter transactions to include only frequent items
    frequent_items_set = set(frequent_items)
    
    # Build a set of frequent pairs for quick lookup
    frequent_pairs_set = set(frequent_pairs)

    for transaction in transactions:
        # Only include items in the transaction that are frequent
        items_in_transaction = set(transaction).intersection(frequent_items_set)
        
        # Generate triplets from the sorted list of frequent items in the transaction
        for triplet in combinations(sorted(items_in_transaction), 3):
            # Check if all subsets of the triplet are frequent
            if all(tuple(sorted(pair)) in frequent_pairs_set for pair in combinations(triplet, 2)):
                global_triplet_counter[triplet] += 1

    # Filter for frequent triplets globally
    frequent_triplets = {triplet for triplet, count in global_triplet_counter.items() if count >= min_support}
    return frequent_triplets
    

    
#pass4
#def C4(transactions, frequent_items, frequent_pairs, frequent_triplets, min_support):
    # Create sets for quick lookup
 #   frequent_items_set = set(frequent_items)
  #  frequent_pairs_set = set(frequent_pairs)
   # frequent_triplets_set = set(frequent_triplets)

    # Build a mapping from items to the triplets they participate in
    #item_to_triplets = defaultdict(list)
    #for triplet in frequent_triplets:
     #   for item in triplet:
      #      item_to_triplets[item].append(triplet)

    # Generate potential quadruplets
    #potential_quadruplets = set()
    #for triplets in item_to_triplets.values():
     #   for triplet1, triplet2 in combinations(triplets, 2):
      #      combined = set(triplet1).union(triplet2)
       #     if len(combined) == 4:
        #        quadruplet = tuple(sorted(combined))
                # Check if all subsets (triplets and pairs) are frequent
         #       all_triplets = all(tuple(sorted(trip)) in frequent_triplets_set for trip in combinations(quadruplet, 3))
          #      all_pairs = all(tuple(sorted(pair)) in frequent_pairs_set for pair in combinations(quadruplet, 2))
           #     if all_triplets and all_pairs:
            #        potential_quadruplets.add(quadruplet)

    # Count occurrences of each candidate quadruplet
    #for transaction in transactions:
     #   transaction_set = set(transaction).intersection(frequent_items_set)
      #  for quadruplet in potential_quadruplets:
       #     if all(item in transaction_set for item in quadruplet):
        #        global_quadruplet_counter[quadruplet] += 1

    # Filter for frequent quadruplets globally
   # frequent_quadruplets = {quad for quad, count in global_quadruplet_counter.items() if count >= min_support}
    #return frequent_quadruplets
    
    

def calculate_confidence_for_triplets(frequent_triplets, global_triplet_counter, global_pair_counter, global_item_counter, total_transactions, min_confidence,record_id):
    print("Association Rules from Triplets and their Confidence Scores:")
    # Use a dictionary to track and print rules only if their confidence has changed and is above the threshold
    if not hasattr(calculate_confidence_for_triplets, "last_printed_confidence"):
        calculate_confidence_for_triplets.last_printed_confidence = {}
    last_printed_confidence = calculate_confidence_for_triplets.last_printed_confidence
   
    for triplet in frequent_triplets:
        triplet_count = global_triplet_counter[triplet]

        # Generate all non-empty proper subsets for antecedents and their complements as consequents
        for antecedent in combinations(triplet, len(triplet) - 1):  # Typically looking at 2-item antecedents
            antecedent = tuple(antecedent)
            consequent = tuple(set(triplet) - set(antecedent))

            # Get counts for antecedent and consequent based on their size
            if len(antecedent) == 1:
                antecedent_count = global_item_counter[antecedent[0]]
            elif len(antecedent) == 2:
                antecedent_count = global_pair_counter[antecedent]
            else:
                continue

            if antecedent_count > 0:
                confidence = triplet_count / antecedent_count
                rule_key = (antecedent, consequent)

                # Check against last printed confidence to avoid duplication
                if (rule_key not in last_printed_confidence or last_printed_confidence[rule_key] != confidence) and confidence >= min_confidence:
                    last_printed_confidence[rule_key] = confidence
                    rule_document = {
                    	'_id': record_id,
                        'antecedent': list(antecedent),
                        'consequent': list(consequent),
                        'confidence': confidence,
                        'count': global_triplet_counter[triplet],
                        'total_transactions': total_transactions
                    }
                    # Insert the document into MongoDB
                    collection.insert_one(rule_document)
                    record_id+=1
                  
                    print(f"Rule: {antecedent} -> {consequent},Count:{global_triplet_counter[triplet]} Confidence: {confidence:.2f}, Support: {triplet_count / total_transactions:.3f}")

                    
                    
    
def consume_messages(consumer, min_support, window_size,min_confidence):
    transactions = []
    total_transactions = 0
    record_id = collection.count_documents({}) + 1
    try:
        for message in consumer:
            data = message.value['also_buy'] + [message.value['asin']]
            transactions.append(data)

            if len(transactions) >= window_size:
                total_transactions += len(transactions)  # Accumulate the total count of transactions

                # First pass: find frequent 1-itemsets
                frequent_items = C1(transactions, min_support)

                # Second pass: find frequent 2-itemsets
                frequent_pairs = C2(transactions, frequent_items, min_support)

                # Third pass: find frequent triples 
                frequent_triplets = C3(transactions, frequent_items, frequent_pairs, min_support)
                
                # Fourth pass : find frequent quad-4 itemsets
                #frequent_quadruplets = C4(transactions, frequent_items, frequent_pairs, frequent_triplets, min_support)
		
                # Clear transactions for the next window
                transactions.clear()
                
                print(f"Processed window with {total_transactions} transactions.")
                calculate_confidence_for_triplets(frequent_triplets, global_triplet_counter, global_pair_counter, global_item_counter, total_transactions, min_confidence,record_id)
                record_id += len(frequent_triplets)
                
		#logss
		
                # Print results for diagnostics
                # print(f"Processed window with {total_transactions} transactions.")
                #print("Frequent Items and their Counts:")
                #for item in frequent_items:
                 #   print(f"Item: {item}, Count: {global_item_counter[item]}")

                #print("Frequent Pairs and their Counts:")
                #for pair in frequent_pairs:
                  #     print(f"Pair: {pair}, Count: {global_pair_counter[pair]}")
                    
                #print("Frequent Triples and their Counts:")
                #for triple in frequent_triplets:
                
  #                      print(f"Triple: {triple}, Count: {global_triplet_counter[triple]},Score : {global_triplet_counter[triple] / total_transactions:.3f}")
                #print("Frequent Quadruplets and their Counts:")
                #for quadruplet in frequent_quadruplets:
        	 #       print(f"Quadruplet: {quadruplet}, Count: {global_quadruplet_counter[quadruplet]}")

                #calculate_confidence(frequent_quadruplets, (global_item_counter, global_pair_counter, global_triplet_counter, global_quadruplet_counter), min_confidence)
        
    except KeyboardInterrupt:
        print("Stopped consuming due to user interruption.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        consumer.close()
        print("Kafka Consumer closed successfully.")


if __name__ == "__main__":

    min_confidence = 0.75
    min_support = 290  # Minimum support threshold
    window_size = 5000  # Manageable window size for processing
    
    consumer = KafkaConsumer(topic,bootstrap_servers=bootstrap_servers,auto_offset_reset='earliest',enable_auto_commit=False,group_id='batchGroup',value_deserializer=lambda x: json.loads(x.decode('utf-8')),max_poll_records=200  # Adjust based on system capabilities
    )

    print(f"Starting to consume messages from {topic}")
    consume_messages(consumer, min_support, window_size,min_confidence)

