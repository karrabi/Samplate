from kafka import KafkaConsumer
import time
import json

import Loader
import Transformer

# Wait for 40 seconds to allow Kafka brokers to start
time.sleep(40)


BATCH_SIZE = 1000 # Number of messages to process in a batch


print('Consumer start ...')

# Define the list of Kafka brokers
brokers = ['kafka1:9092', 'kafka2:9092', 'kafka3:9092']
# Create a Kafka consumer instance
consumer = KafkaConsumer(
    'crypto_topic', 'forex_topic',
    bootstrap_servers=brokers,
    auto_offset_reset='earliest',  # Start consuming from the earliest available message
    enable_auto_commit=False,  # Disable auto-commit to ensure at-least-once delivery
    group_id='my-group',  # Consumer group ID for load balancing
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),  # Deserialize JSON messages
    fetch_max_bytes=52428800,  # 50MB max fetch size
    max_poll_records=5000,  # Max number of records to fetch in a single poll
    fetch_max_wait_ms=500,  # Max time to wait for fetch
    fetch_min_bytes=1  # Fetch at least 1 byte (don't wait for more data)
)

print('Consumer configured ...')

def main():
    """
    Main function to run the Kafka consumer and process messages.
    """
    while True:
        messages = consumer.poll(timeout_ms=1000, max_records=BATCH_SIZE)
        if not messages:
            continue

        for topic_partition, records in messages.items():
            print(f"{len(records)} Records received")
            transformed_records = Transformer.transform(records)
            Loader.loadToDatabase(transformed_records)

        consumer.commit()  # Commit offsets after processing all batches

if __name__ == "__main__":
    main()