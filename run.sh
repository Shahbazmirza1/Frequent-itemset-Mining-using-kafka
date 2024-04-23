#!/bin/bash

# Path to Kafka and MongoDB directories
KAFKA_DIR="$HOME/Downloads/kafka"
MONGODB_DIR="/var/lib/mongodb"

# Start MongoDB
echo "Starting MongoDB..."
sudo systemctl start mongod

# Start Zookeeper for Kafka
echo "Starting Zookeeper for Kafka..."
"$KAFKA_DIR"/bin/zookeeper-server-start.sh "$KAFKA_DIR"/config/zookeeper.properties &

sleep 5  # Wait for Zookeeper to start

# Start Kafka Server
echo "Starting Kafka Server..."
"$KAFKA_DIR"/bin/kafka-server-start.sh "$KAFKA_DIR"/config/server.properties &

sleep 5  # Wait for Kafka Server to start

# Create Kafka Topic
echo "Creating Kafka Topic..."
"$KAFKA_DIR"/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic amazon_data

# Change directory to the project folder
cd "$HOME/Downloads/Frequent-itemset-Mining-using-kafka"

# Start Producer for Algorithm Application
echo "Starting Producer for Algorithm Application..."
python producer.py &

sleep 5  # Wait for Producer to start

# Start Consumer for Apriori Algorithm
echo "Starting Consumer for Apriori Algorithm..."
python consumer_apriori.py &

# Start Consumer for PCY Algorithm
echo "Starting Consumer for PCY Algorithm..."
python consumer_pcy.py &

# Start Innovative Consumer
echo "Starting Innovative Consumer..."
python consumer_innovative.py &

echo "All components started successfully!"
