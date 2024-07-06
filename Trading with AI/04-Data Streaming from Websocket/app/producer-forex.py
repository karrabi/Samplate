import websocket
from kafka import KafkaProducer
import json
import time

# An samll delay to Kafka servers get ready
time.sleep(30)

# Initialize Kafka producer
brokers = ['kafka1:9092', 'kafka2:9092']
producer = KafkaProducer(
    bootstrap_servers=brokers
    )


def on_message(ws, message):
    """
    Callback function for handling incoming WebSocket messages.

    Args:
        ws: WebSocket connection object.
        message (str): Received message in JSON format.

    """
    dict_message = json.loads(message)

    # Iterate through data rows and send them to Kafka topic
    if dict_message['type'] == 'trade':
        for row in dict_message['data']:
            print(row)
            message_bytes = json.dumps(row).encode('utf-8')
            producer.send('test-topic', message_bytes)
    else:
        print(message)
        
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
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:41"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:10026"}')
    ws.send('{"type":"subscribe","symbol":"OANDA:XAU_USD"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:XAU/USD"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:BTC/USD"}')




if __name__ == "__main__":
    
    print('Producer Start ...')
    
    # Set up WebSocket connection
    websocket.enableTrace(False)
    while True:
        try:

            ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c5dshh2ad3ifm1hm82s0",
                                    on_message = on_message,
                                    on_error = on_error)
            ws.on_open = on_open
            ws.run_forever()
            
        except Exception as e:
            print(f"Connection lost: {e}. Reconnecting...")
            time.sleep(5)  # Wait for 5 seconds before attempting to reconnect

