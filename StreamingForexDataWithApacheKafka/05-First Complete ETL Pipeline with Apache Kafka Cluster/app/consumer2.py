from kafka import KafkaConsumer
import time
import json

import psycopg2
from psycopg2 import pool

# Define the list of Kafka brokers
brokers = ['kafka1:9092', 'kafka2:9092', 'kafka3:9092']

# Wait for 40 seconds to allow Kafka brokers to start
time.sleep(40)

print('Consumer start ...')

# Create a Kafka consumer instance
consumer = KafkaConsumer(
    'crypto_topic', 'forex_topic',  # Subscribe to the 'crypto_topic' and 'forex_topic' topics
    bootstrap_servers=brokers,
    auto_offset_reset='earliest',  # Start consuming messages from the earliest available offset
    enable_auto_commit=False,  # Disable automatic offset committing
    group_id='my-group',  # Assign the consumer to a consumer group
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Deserialize the message value from JSON
)

print('Consumer configured ...')

# Create a connection pool to the PostgreSQL database
connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host="postgres",
    database="tradingmarketdata",
    user="postgres",
    password="postgres"
)

# Set the batch size for message processing
BATCH_SIZE = 1000

# Run the consumer in an infinite loop
while True:
    # Consume messages in batches
    messages = consumer.poll(timeout_ms=1000, max_records=BATCH_SIZE)

    # If no messages are available, continue to the next iteration
    if not messages:
        continue

    # Get a connection from the connection pool
    conn = connection_pool.getconn()

    try:
        with conn.cursor() as cur:
            # Begin a database transaction
            cur.execute("BEGIN")

            # Iterate through the received messages
            for topic_partition, records in messages.items():
                for record in records:
                    # Process the message and insert/update records in the database
                    message_value = record.value
                    cur.execute(f"INSERT INTO trades (price, symbol, time, volume) VALUES ({message_value['p']}, '{message_value['s']}', {message_value['t']}, {message_value['v']})")
                    print(f"Received message: {record.topic} - {record.partition} - {message_value}")

            # Commit the database transaction if all messages are processed successfully
            cur.execute("COMMIT")

        # Commit the Kafka offsets after the successful database transaction
        consumer.commit()

    except Exception as e:
        # Rollback the database transaction if any error occurs
        conn.rollback()
        # Handle the error, implement retries, or send messages to a dead-letter queue
        print(f"Error: {e}")

    finally:
        # Return the connection to the connection pool
        connection_pool.putconn(conn)
