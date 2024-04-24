#!/bin/bash

# Terminal 1: Start Zookeeper server
echo "Starting Zookeeper for Kafka..."
gnome-terminal -- bash -c "cd /home/shahbaz/kafka; \
while true; do \
  bin/zookeeper-server-start.sh config/zookeeper.properties; \
  if [ $? -eq 0 ]; then \
    break; \
  else \
    echo 'Zookeeper failed to start, retrying...'; \
    sleep 5; \
  fi; \
done; \
exec bash"

# Wait for 10 seconds before starting Kafka server
sleep 5

# Terminal 2: Start Kafka server

echo "Starting Kafka Server..."
gnome-terminal -- bash -c "cd /home/shahbaz/kafka; \
while true; do \
  bin/kafka-server-start.sh config/server.properties; \
  if [ $? -eq 0 ]; then \
    break; \
  else \
    echo 'Kafka server failed to start, retrying...'; \
    sleep 5; \
  fi; \
done; \
exec bash"

sleep 2


# Terminal 3: Start and check status of MongoDB
echo "Starting MongoDB..."
gnome-terminal -- bash -c "while true; do \
  sudo systemctl start mongod; \
  if [ $? -eq 0 ]; then \
    break; \
  else \
    echo 'Failed to start MongoDB, retrying...'; \
    sleep 5; \
  fi; \
done; \
sleep 2; \
sudo systemctl status mongod; \
exec bash"
