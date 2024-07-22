from kafka import KafkaConsumer
import redis

import time
import datetime

cache = redis.Redis(host='redis', port=6379, db=0)

brokers = ['kafka1:9092', 'kafka2:9092', 'kafka3:9092']

print('Waiting for Kafka Brokers to start ...')
time.sleep(30)

print('Consumer start ...')
consumer = KafkaConsumer(
    'crypto_topic', 'forex_topic', # Subscribe to the 'crypto_topic' and 'forex_topic' topics
    bootstrap_servers=brokers,
    auto_offset_reset='earliest', # Start consuming messages from the earliest available offset
    enable_auto_commit=True,
    group_id='my-group'
)

for message in consumer:
    now = datetime.datetime.now()
    t = int(time.time()) * 1000
    print(f"{now}: Received message: {message.topic}: {message.value.decode('utf-8')}")
    try:
        cache.zadd(message.topic, {str(t): float(message.value.decode('utf-8'))})
    except Exception as e:
        print(f'Error: {e}')
