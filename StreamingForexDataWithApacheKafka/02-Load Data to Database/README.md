
# Simple Apache Kafka Cluster

This project provides a basic setup for an Apache Kafka Cluster, including an Apache Kafka broker, Zookeeper, a producer, and a consumer. The Kafka broker and Zookeeper run inside Docker containers, while the producer and consumer interact with Kafka on the local machine.

## Project Structure

### Inside Docker

1. **Apache Kafka Broker**: The Kafka broker runs inside a Docker container.
2. **Zookeeper**: Zookeeper, which is essential for Kafka coordination, also runs inside a Docker container.
3. **PostgreSQL**: The PostgreSQL server runs inside a Docker container.
4. **PGAdmin**: The PGAdmin, to access PostgreSQL database, runs inside a Docker container.

### Outside Docker

1. **Producer**: A Python script that generates messages for Kafka.
2. **Consumer**: Another Python script that consumes messages from Kafka.
![structure](../images/Step%2002.gif)

## How to Run

Follow these steps to set up and run the Kafka Cluster:

1. **Clone the Repository**:
   - Clone the repository:
   ```bash
   git clone https://github.com/karrabi/Samplate.git
   cd Samplate/StreamingForexDataWithApacheKafka
   ```


2. **Setup Kafka Cluster**:
   - Open a command prompt inside *Samplate/StreamingForexDataWithApacheKafka* folder.
   - Run the following command to start the Kafka broker and Zookeeper containers:
     ```bash
     docker compose up
     ```

3. **Prepare Producer and Consumer**:
   - Open another command prompt inside *Samplate/StreamingForexDataWithApacheKafka* folder.
   - Create a virtual environment for Python:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     ```bash
     venv\Scripts\Activate
     ```
   - Install the necessary Python packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Producers**:
   - In the same command prompt, activate the virtual environment again:
     ```bash
     venv\Scripts\Activate
     ```
   - Run the first producer script:
     ```bash
     python producer-forex.py
     ```
   - Open another command prompt inside the project folder.
   - Activate the virtual environment:
     ```bash
     venv\Scripts\Activate
     ```
   - Run the second producer script:
     ```bash
     python producer-crypto.py
     ```
5. **Run the Consumer**:
   - Open another command prompt inside the project folder.
   - Activate the virtual environment:
     ```bash
     venv\Scripts\Activate
     ```
   - Run the consumer script:
     ```bash
     python consumer.py
     ```

6. **Stop and Clean the environment**:
   - Open a command prompt inside the project folder.
   - Run the following command to stop the Kafka broker and Zookeeper containers:
     ```bash
     docker-compose down
     ```
