from kafka import KafkaConsumer
import redis
import time
import json
from concurrent.futures import ThreadPoolExecutor
import psycopg2
from psycopg2 import pool

import symbols

# Wait for 40 seconds to allow Kafka brokers to start
time.sleep(40)

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

# Create a connection pool to the PostgreSQL database
connection_pool = pool.SimpleConnectionPool(
    minconn=1,   # Minimum number of connections in the pool
    maxconn=10,  # Maximum number of connections in the pool
    host="postgres",
    database="mltrading",
    user="postgres",
    password="postgres"
)

# Create a connection to Redis as cache
cache = redis.Redis(host='redis', port=6379, db=0)

BATCH_SIZE = 1000 # Number of messages to process in a batch

def process_message(message_value):
    """
    Process a single message and update Redis cache.

    Args:
        message_value (dict): The message value containing trade data.
    """
    symbol = symbols.PAIRS[message_value['s']]
    lkey = f"lastPrice:{symbol}"
    cache.set(lkey, float(message_value['p']))
    hkey = f"historyPrice:{symbol}"
    value = f"{str(message_value['p'])}:{message_value['t']}"
    cache.zadd(hkey, {value: message_value['t']})


def process_batch(records):
    """
    Process a batch of records, inserting them into the database and updating Redis.

    Args:
        records (list): A list of Kafka consumer records to process.
    """
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("BEGIN")
            for record in records:
                print(f"Record Received: {record}")
                message_value = record.value
                symbol = symbols.PAIRS[message_value['s']]
                cur.execute("INSERT INTO trades (price, symbol, time, volume) VALUES (%s, %s, %s, %s)",
                            (message_value['p'], symbol, message_value['t'], message_value['v']))
                process_message(message_value)
            cur.execute("COMMIT")
    except Exception as e:
        conn.rollback()
        print(f"Error processing batch: {e}")
    finally:
        connection_pool.putconn(conn)

def main():
    """
    Main function to run the Kafka consumer and process messages.
    """
    while True:
        messages = consumer.poll(timeout_ms=1000, max_records=BATCH_SIZE)
        if not messages:
            continue

        for topic_partition, records in messages.items():
            process_batch(records)

        consumer.commit()  # Commit offsets after processing all batches

if __name__ == "__main__":
    main()