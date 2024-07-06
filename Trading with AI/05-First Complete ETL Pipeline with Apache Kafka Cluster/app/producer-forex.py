import websocket

from kafka import KafkaProducer
import time
import json


# Wait for 40 seconds to allow Kafka brokers to start
time.sleep(40)

# Define the list of Kafka brokers
brokers = ['kafka1:9092', 'kafka2:9092', 'kafka3:9092']

# Create a Kafka producer instance
producer = KafkaProducer(
    bootstrap_servers=brokers
)


def on_message(ws, message):
    """
    Callback function to handle incoming WebSocket messages.

    Args:
        ws (websocket.WebSocketApp): The WebSocket application instance.
        message (str): The received message.
    """
    try:
        # Parse the incoming message as JSON
        dict_message = json.loads(message)

        # Iterate through the data rows in the message
        for row in dict_message['data']:
            # Print the row
            print(row)

            # Convert the row to a JSON-encoded byte string and send it to the 'crypto_topic' Kafka topic
            message_bytes = json.dumps(row).encode('utf-8')
            producer.send('crypto_topic', message_bytes)
    except Exception as e:
        # Print any exceptions that occur during message processing
        print(e)
        print(message)


def on_error(ws, error):
    """
    Callback function to handle WebSocket errors.

    Args:
        ws (websocket.WebSocketApp): The WebSocket application instance.
        error (str): The error message.
    """
    print(f'Error: {error}')


def on_close(ws):
    """
    Callback function to handle WebSocket connection closure.

    Args:
        ws (websocket.WebSocketApp): The WebSocket application instance.
    """
    print("### closed ###")


def on_open(ws):
    """
    Callback function to handle WebSocket connection opening.
    Sends subscription requests for the specified trading pairs.

    Args:
        ws (websocket.WebSocketApp): The WebSocket application instance.
    """
    # Subscribe to some forex trading pairs
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:41"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:10026"}')
    ws.send('{"type":"subscribe","symbol":"OANDA:XAU_USD"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:XAU/USD"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:BTC/USD"}')


if __name__ == "__main__":
    # Print a message to indicate that the producer is starting
    print('Producer Start ...')

    # Disable WebSocket trace logging
    websocket.enableTrace(False)

    # Run the WebSocket application in an infinite loop, reconnecting if the connection is lost
    while True:
        try:
            # Create a WebSocket application instance and set the callback functions
            ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=bpu4no7rh5red6hq49u0",
                                        on_message=on_message,
                                        on_error=on_error)
            ws.on_open = on_open
            ws.run_forever()
        except Exception as e:
            # Print a message to indicate that the connection was lost and attempt to reconnect
            print(f"Connection lost: {e}. Reconnecting...")
            time.sleep(5)  # Wait for 5 seconds before attempting to reconnect
