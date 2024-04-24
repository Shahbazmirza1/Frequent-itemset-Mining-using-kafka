# Streaming Data Insights with Frequent Itemset Analysis on Amazon

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Overview

This repository contains the code and documentation for a streaming data analysis project focusing on frequent itemset mining applied to Amazon Metadata. The project utilizes advanced algorithms to extract insights and associations from streaming data in real-time.

## Dataset

The Amazon Metadata dataset provides rich information about products, including attributes such as product ID (`asin`), title, features, description, price, image URLs, related products, sales rank, brand, categories, and technical details. The dataset is provided in JSON format.

## Data Preprocessing
1. consumerPreprocess.py utilizes a Kafka consumer to ingest data from the amazon_data topic, preprocesses each message, and stores the processed data into MongoDB. This real-time processing pipeline ensures that the dataset remains up-to-date and ready for further analysis and insights extraction. The preprocessing steps include:
   -  Removing specific columns (e.g., "description", "price", "imageURL") from the dataset.
   -  Cleaning HTML tags and JavaScript content from text fields.
   -  Normalizing and preparing the data for storage in MongoDB.
2. The producerPreprocess.py script serves as a producer application responsible for preprocessing and sending data from a JSON file to a Kafka topic named amazon_data. This script is an essential component of the streaming data processing pipeline, ensuring that raw data is ingested, processed, and made available for analysis in real-time.

## Algorithm Implementation

producer.py script is dedicated to feeding data for three distinct algorithms – Apriori, PCY, and an innovative algorithm – applied to the Amazon dataset.

### Functionality

- **Data Source**: Connects to MongoDB to access the Amazon product dataset.
  
- **Data Publication**: Publishes extracted data to the Kafka topic for consumption by the algorithm-specific consumers.

Producer serves as the cornerstone for algorithmic analysis on the Amazon dataset, enabling the subsequent application of various algorithms for insights extraction.


## Tools Used

- **Python**: For coding the producer and consumer applications, as well as implementing the Apriori and PCY algorithms.
- **Kafka**: As the messaging system for real-time data streaming.
- **MongoDB**: As the database solution for storing the results of frequent itemset mining.
- **JSON**: For handling the dataset, which is provided in JSON format.
- **Git**: For version control and collaboration.

## Setup Instructions

1. **Downloading and Sampling the Dataset**:
   - Download the Amazon Metadata dataset from [here](link).
   - Extract the dataset. Ensure that the extracted size is at least 15 GB.
   - Sample the dataset using the provided script.

2. **Pre-Processing**:
   - Load the sampled dataset.
   - Preprocess the data to clean and format it for analysis.
   - Generate a new JSON file containing the preprocessed data.

3. **Kafka Setup**:
   - Start Zookeeper:
     ```bash
     cd kafka_directory
     bin/zookeeper-server-start.sh config/zookeeper.properties
     ```

   - Start Kafka Server:
     ```bash
     cd kafka_directory
     bin/kafka-server-start.sh config/server.properties
     ```

   - Create Kafka Topic:
     ```bash
     cd kafka_directory
     bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic processed
     ```

4. **Running the Code**:
   - **Start MongoDB**:
     ```bash
     sudo systemctl start mongod
     ```

   - **Start Zookeeper**:
     ```bash
     cd kafka_directory
     bin/zookeeper-server-start.sh config/zookeeper.properties
     ```

   - **Start Kafka Server**:
     ```bash
     cd kafka_directory
     bin/kafka-server-start.sh config/server.properties
     ```

   - **Create Kafka Topic**:
     ```bash
     cd kafka_directory
     bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic processed
     ```

   - **Run Producer Application**:
     ```bash
     python producer_kafka.py
     ```

   - **Run Consumer Applications**:
     ```bash
     python consumer_apriori.py
     python consumer_pcy.py
     python consumer_innovative.py
     ```

5. **Auto-mate the above code**:
    - **Running the bash-script**:
      ```bash
      ./run.sh
      be sure to read the run.sh toadjust paths
     ```

## License

This project is licensed under the [Apache License 2.0](https://opensource.org/licenses/Apache-2.0). See the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss the proposed changes.

---
This README provides detailed instructions for setting up and running the Streaming Data Insights project with Kafka integration. For additional information, please refer to the project repository.
