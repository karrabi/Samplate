
# Simple Apache Kafka Cluster

This project provides a basic setup for an Apache Kafka Cluster, including an Apache Kafka broker, Zookeeper, a producer, and a consumer. The Kafka broker and Zookeeper run inside Docker containers, while the producer and consumer interact with Kafka on the local machine.

## Project Structure

1. **Apache Kafka Broker 1**: The Kafka broker, runs inside a Docker container.
1. **Apache Kafka Broker 2**: Another Kafka broker, runs inside a Docker container.
2. **Zookeeper**: Zookeeper, which is essential for Kafka coordination, also runs inside a Docker container.
3. **Producer**: A Python script that generates messages for Kafka, runs inside a Docker container.
4. **Consumer**: Another Python script that consumes messages from Kafka, runs inside a Docker container.
![structure](../images/Step%2003.gif)

## How to Run

Follow these steps to set up and run the Kafka Cluster:

1. **Clone the Repository**:
   - Clone the repository:
   ```bash
   git clone https://github.com/karrabi/Samplate.git
   cd Samplate/StreamingForexDataWithApacheKafka
   ```


2. **Setup Project**:
   - Open a command prompt inside *Samplate/StreamingForexDataWithApacheKafka* folder.
   - Run the following command to start the Kafka broker and Zookeeper containers:
     ```bash
     docker compose up
     ```

3. **Stop and Clean the environment**:
   - Open a command prompt inside the project folder.
   - Run the following command to stop the Kafka broker and Zookeeper containers:
     ```bash
     docker-compose down
     ```
