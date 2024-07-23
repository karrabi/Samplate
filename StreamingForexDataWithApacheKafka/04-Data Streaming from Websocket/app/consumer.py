# consumer/consumer.py
from kafka import KafkaConsumer
import time
import datetime
import logging
import json
import ast


import psycopg2
from psycopg2 import pool

time.sleep(30)

# Initialize Kafka producer
print('Consumer start initiating...')
brokers = ['kafka1:9092', 'kafka2:9092']
consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers=brokers,
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    group_id='my-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))

)


print('Consumer initiated ...')


connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host="postgres",
    database="tradingmarketdata",
    user="postgres",
    password="postgres"
)

# for message in consumer:
#     print(message)


BATCH_SIZE = 1000

while True:
    # Consume messages in batches
    messages = consumer.poll(timeout_ms=1000, max_records=BATCH_SIZE)

    if not messages:
        continue

    conn = connection_pool.getconn()
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
        connection_pool.putconn(conn)
