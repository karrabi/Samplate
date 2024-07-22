from kafka import KafkaProducer
import time

def main():
    """
    Kafka Producer Example

    This script sends messages to a Kafka topic ('test-topic') at regular intervals.

    Prerequisites:
    - Kafka broker running on localhost:9092
    - Python Kafka library installed (use 'pip install kafka-python')

    Usage:
    - Run this script to start producing messages.
    - Adjust the topic name and message content as needed.
    - Press Ctrl+C to stop the producer.

    Note: In a real-world scenario, you'd handle exceptions and configure additional settings.

    """

    print('Producer Start ...')
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    i = 1
    try:
        while True:
            message = f'Hello, Kafka! Message {i}'
            print(f'Sending message {i}: {message}')
            producer.send('test-topic', message.encode('utf-8'))
            print("Message sent")
            time.sleep(5)
            i += 1
    except KeyboardInterrupt:
        print("\nProducer stopped by user.")
    finally:
        producer.close()

if __name__ == "__main__":
    main()
