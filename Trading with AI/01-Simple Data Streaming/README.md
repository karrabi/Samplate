
# Simple Apache Kafka Farm

This project provides a basic setup for an Apache Kafka farm, including an Apache Kafka broker, Zookeeper, two producers, and a consumer. The Kafka broker and Zookeeper run inside Docker containers, while the producers and consumer interact with Kafka on the local machine on port 9092.

updates:
- added two producers
- producers fetch trading market data from a websocket. 
  you can access the websocket documentation here:(https://finnhub.io/docs/api/websocket-trades)


## Project Structure

### Inside Docker

1. **Apache Kafka Broker**: The Kafka broker runs inside a Docker container.
2. **Zookeeper**: Zookeeper, which is essential for Kafka coordination, also runs inside a Docker container.

### Outside Docker

1. **Producer**: A Python script that generates Kafka messages.
2. **Consumer**: Another Python script that consumes Kafka messages.

## How to Run

Follow these steps to set up and run the Kafka farm:

1. **Clone the Project**:
   - Clone this project to your local machine.
    ```
    git clone https://github.com/karrabi/Samplates.git
    ```
2. **Setup Kafka Farm**:
   - Open a command prompt inside the project folder.
   - Run the following command to start the Kafka broker and Zookeeper containers:
     ```
     docker-compose up
     ```

3. **Prepare Producer and Consumer**:
   - Open another command prompt inside the project folder.
   - Create a virtual environment for Python (if you haven't already):
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
     ```
     venv\Scripts\Activate
     ```
   - Install the necessary Python packages:
     ```
     pip install -r requirements.txt
     ```

4. **Run the Producers**:
   - In the same command prompt, activate the virtual environment again:
     ```
     venv\Scripts\Activate
     ```
   - Run the producer script:
     ```
     python producer-btc.py
     ```

   - In the another command prompt, activate the virtual environment again:
     ```
     venv\Scripts\Activate
     ```
   - Run the producer script:
     ```
     python producer-eur.py
     ```

5. **Run the Consumer**:
   - Open another command prompt inside the project folder.
   - Activate the virtual environment:
     ```
     venv\Scripts\Activate
     ```
   - Run the consumer script:
     ```
     python consumer.py
     ```

6. **Stop and Clean Kafka Farm**:
   - Open a command prompt inside the project folder.
   - Run the following command to stop the Kafka broker and Zookeeper containers:
     ```
     docker-compose down
     ```

Feel free to customize this `README.md` further based on any additional details you'd like to provide.




