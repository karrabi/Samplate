from kafka import KafkaConsumer
import datetime

def main():
    """
    Kafka Consumer Example

    This script consumes messages from a Kafka topic ('test-topic') and prints them to the console.

    Prerequisites:
    - Kafka broker running on localhost:9092
    - Python Kafka library installed (use 'pip install kafka-python')

    Usage:
    - Run this script to start consuming messages.
    - Adjust the topic name and other settings as needed.
    - Press Ctrl+C to stop the consumer.

    Note: In a real-world scenario, you'd handle exceptions and process the messages as required.

    """
    print('Consumer start ...')
    consumer = KafkaConsumer(
        'test-topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group'
    )

    try:
        for message in consumer:
            now = datetime.datetime.now()
            decoded_message = message.value.decode('utf-8')
            print(f"{now}: Received message: {decoded_message}")
    except KeyboardInterrupt:
        print("\nConsumer stopped by user.")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
