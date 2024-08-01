# consumer/consumer.py
from kafka import KafkaConsumer
import time
import datetime
import logging

brokers = ['kafka1:9092', 'kafka2:9092']

print('Waiting for Kafka Brokers to start ...')
time.sleep(30)

print('Consumer start ...')
consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers=brokers,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group'
)

for message in consumer:
    now = datetime.datetime.now()

    print(f"{now}: Received message: {message.value.decode('utf-8')}")
