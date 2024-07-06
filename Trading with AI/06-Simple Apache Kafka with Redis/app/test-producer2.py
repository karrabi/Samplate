from kafka import KafkaProducer
import time
import datetime

print('Waiting for Kafka Brokers to start ...')
time.sleep(30)

print('Producer Start ...')

# Define Kafka brokers
brokers = ['kafka1:9092', 'kafka2:9092', 'kafka3:9092']
producer = KafkaProducer(bootstrap_servers=brokers)


i = 1
while True:
    now = datetime.datetime.now()
    print(f'Sending message {i} ...')
    message = str(i).encode('utf-8')
    producer.send('forex_topic', message) # Send data to Kafka topic 'crypto_topic'
    print("Message sent")
    time.sleep(0.1)
    i += 1
