from kafka import KafkaProducer
import time
import datetime

print('Waiting for Kafka Brokers to start ...')
time.sleep(30)

print('Producer Start ...')

brokers = ['kafka1:9092', 'kafka2:9092']
producer = KafkaProducer(bootstrap_servers=brokers)


i = 1
while True:
    now = datetime.datetime.now()
    print(f'Sending message {i} ...')
    producer.send('test-topic', b'Hello, Kafka! from producer 1')
    print("Message sent")
    time.sleep(0.1)
    i += 1
