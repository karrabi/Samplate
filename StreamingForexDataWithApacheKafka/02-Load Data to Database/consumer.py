from kafka import KafkaConsumer
import datetime
import json
import psycopg2
from psycopg2 import pool

# Configure database connection pool
pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    database="tradingmarketdata",
    user="postgres",
    password="postgres",
)

BATCH_SIZE = 1000

def main():
    """
    Kafka Consumer Example

    This script consumes messages from a Kafka topic ('test-topic') and prints them to the console.

    Prerequisites:
    - Kafka broker running on localhost:9092
    - Python Kafka library installed (use 'pip install kafka-python')

    Usage:
    - Run this script to start consuming messages.
        just the topic name and other settings as needed.
    - Press Ctrl+C to stop the consumer.

    Note: In a real-world scenario, you'd handle exceptions and process the messages as required.

    """
    print('Consumer start ...')
    consumer = KafkaConsumer(
        'test-topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    while True:
        # Consume messages in batches
        messages = consumer.poll(timeout_ms=1000, max_records=BATCH_SIZE)

        if not messages:
            continue

        conn = pool.getconn()
        try:
            with conn.cursor() as cur:
                # Begin a transaction
                cur.execute("BEGIN")

                for topic_partition, records in messages.items():
                    for record in records:
                        # Process the message and insert/update records in the database
                        message_value = record.value
                        cur.execute(f"INSERT INTO trades (price, symbol, time, volume) VALUES ({message_value['p']}, '{message_value['s']}', {message_value['t']}, {message_value['v']})")
                        print(f"Received message: {message_value}")

                # Commit the transaction if all messages are processed successfully
                cur.execute("COMMIT")

            # Commit Kafka offsets after successful database transaction
            consumer.commit()

        except Exception as e:
            # Rollback the transaction if any error occurs
            conn.rollback()
            # Handle the error, implement retries, or send messages to a dead-letter queue
            print(f"Error: {e}")

        finally:
            # Return the connection to the pool
            pool.putconn(conn)

if __name__ == "__main__":
    main()
