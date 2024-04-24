# Streaming Data Insights with Frequent Itemset Analysis on Amazon

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Table of Contents

|    | Section                                  |
|----|------------------------------------------|
| 1. | [Overview](#overview)                    |
| 2. | [Contributors](#contributors)            |
| 3. | [Dataset](#dataset)                      |
| 4. | [Data Preprocessing](#data-preprocessing)|
| 5. | [Algorithm Implementation](#algorithm-implementation) |
| 5.1 | [Apriori Algorithm](#apriori-algorithm) |
| 5.2 | [PCY Algorithm](#pcy-algorithm)         |
| 6. | [Tools Used](#tools-used)                |
| 7. | [Setup Instructions](#setup-instructions)|
| 8. | [License](#license)                      |
| 9. | [Contributions](#contributions)          |
| 10.| [Additional Information](#additional-information) |


## Contributors

- **I21-2674 Shahbaz Haider Mirza**
- **I21-1365 Talha Rashid**
- **I21-1359 Mirza Nehan**


## Dataset

The Amazon Metadata dataset provides rich information about products, including attributes such as product ID (`asin`), title, features, description, price, image URLs, related products, sales rank, brand, categories, and technical details. The dataset is provided in JSON format.

## Data Preprocessing
1. consumerPreprocess.py utilizes a Kafka consumer to ingest data from the amazon_data topic, preprocesses each message, and stores the processed data into MongoDB. This real-time processing pipeline ensures that the dataset remains up-to-date and ready for further analysis and insights extraction. The preprocessing steps include:
   -  Removing specific columns (e.g., "description", "price", "imageURL") from the dataset.
   -  Cleaning HTML tags and JavaScript content from text fields.
   -  Normalizing and preparing the data for storage in MongoDB.
2. The producerPreprocess.py script serves as a producer application responsible for preprocessing and sending data from a JSON file to a Kafka topic named amazon_data. This script is an essential component of the streaming data processing pipeline, ensuring that raw data is ingested, processed, and made available for analysis in real-time.

## Algorithm Implementation

### Apriori Algorithm

The project employs the classic Apriori algorithm for mining frequent itemsets from streaming data. It iteratively generates candidate itemsets and prunes those that do not meet a minimum support threshold.

#### Approach Overview

- Iteratively identifies frequent itemsets from the streaming Amazon Metadata dataset.
- Employs a series of passes to discover frequent itemsets and association rules.
- Utilizes a sliding window approach to process streaming data efficiently.

#### Implementation Details

- Data is ingested from the Kafka topic `processed`.
- Transactions are constructed from product information, including associated products and product IDs.
- Frequent itemsets are generated through multiple passes over the transaction data.
- Association rules are derived from frequent itemsets, and confidence scores are calculated to measure rule strength.

### PCY Algorithm

The PCY (Park-Chen-Yu) algorithm is a memory-efficient variant of Apriori that utilizes a hash-based counting technique to reduce memory usage.

#### Approach Overview

- Extends Apriori by introducing a hash table to count pairs of items.
- Operates in two passes over the transaction data to count item pairs and filter candidate itemsets efficiently.

#### Implementation Details

- Counts occurrences of item pairs in the first pass using a hash table.
- Filters candidate itemsets based on hash table counts in the second pass.
- Achieves memory efficiency by storing counts in a hash table instead of the entire transaction database.




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
