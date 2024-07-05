import websocket
from kafka import KafkaProducer
import json

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')


def on_message(ws, message):
    """
    Callback function for handling incoming WebSocket messages.

    Args:
        ws: WebSocket connection object.
        message (str): Received message in JSON format.

    """
    dict_message = json.loads(message)

    # Iterate through data rows and send them to Kafka topic
    for row in dict_message['data']:
        print(row)
        message_bytes = json.dumps(row).encode('utf-8')
        producer.send('test-topic', message_bytes)

def on_error(ws, error):
    """
    Callback function for handling WebSocket errors.

    Args:
        ws: WebSocket connection object.
        error (Exception): Error information.

    """
    print(error)

def on_close(ws):
    """
    Callback function when WebSocket connection is closed.

    Args:
        ws: WebSocket connection object.

    """
    print("### closed ###")

def on_open(ws):
    """
    Callback function when WebSocket connection is opened.

    Args:
        ws: WebSocket connection object.

    """
    # Subscribe to specific symbols (customize as needed)
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:2"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:3"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:4"}')



if __name__ == "__main__":
    
    print('Producer Start ...')
    
    # Set up WebSocket connection
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c5dshh2ad3ifm1hm82s0",
                              on_message = on_message,
                              on_error = on_error)
    ws.on_open = on_open
    ws.run_forever()

