# Streaming Data Insights with Frequent Itemset Analysis on Amazon

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Overview

This repository contains the code and documentation for a streaming data analysis project focusing on frequent itemset mining applied to Amazon Metadata. The project utilizes advanced algorithms to extract insights and associations from streaming data in real-time.

## Dataset

The Amazon Metadata dataset provides rich information about products, including attributes such as product ID (`asin`), title, features, description, price, image URLs, related products, sales rank, brand, categories, and technical details. The dataset is provided in JSON format.

## Project Objectives

1. **Downloading and Sampling the Dataset**: Download the Amazon Metadata dataset, sample it, and preprocess it for analysis.
2. **Pre-Processing**: Clean and format the sampled data, ensuring it is suitable for streaming and frequent itemset mining.
3. **Streaming Pipeline Setup**: Develop a producer application to stream preprocessed data in real-time, with three consumer applications subscribing to the data stream.
4. **Frequent Itemset Mining**:
   - Implement the Apriori algorithm in one consumer, providing real-time insights and associations.
   - Implement the PCY algorithm in another consumer, offering real-time insights and associations.
   - Implement innovative analysis in the third consumer, exploring advanced techniques for extracting insights from streaming data.
5. **Database Integration**: Integrate with a non-relational database (e.g., MongoDB) to store the results of frequent itemset mining.

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

## License

This project is licensed under the [Apache License 2.0](https://opensource.org/licenses/Apache-2.0). See the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss the proposed changes.

---
This README provides detailed instructions for setting up and running the Streaming Data Insights project with Kafka integration. For additional information, please refer to the project repository.
