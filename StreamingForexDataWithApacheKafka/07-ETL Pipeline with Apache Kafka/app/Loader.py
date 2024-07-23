import redis
from concurrent.futures import ThreadPoolExecutor
import psycopg2
from psycopg2 import pool

# Create a connection pool to the PostgreSQL database
connection_pool = pool.SimpleConnectionPool(
    minconn=1,   # Minimum number of connections in the pool
    maxconn=10,  # Maximum number of connections in the pool
    host="postgres",
    database="tradingmarketdata",
    user="postgres",
    password="postgres"
)

# Create a connection to Redis as cache
cache = redis.Redis(host='redis', port=6379, db=0)


def loadToRedis(message_value):
    """
    Process a single message and update Redis cache.

    Args:
        message_value (dict): The message value containing trade data.
    """
    lkey = f"lastPrice:{message_value['s']}"
    cache.set(lkey, float(message_value['p']))
    hkey = f"historyPrice:{message_value['s']}"
    value = f"{str(message_value['p'])}:{message_value['t']}"
    cache.zadd(hkey, {value: message_value['t']})



def loadToDatabase(records):
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
                cur.execute("INSERT INTO trades (price, symbol, time, volume) VALUES (%s, %s, %s, %s)",
                            (record['p'], record['s'], record['t'], record['v']))
                loadToRedis(record)
            cur.execute("COMMIT")
    except Exception as e:
        conn.rollback()
        print(f"Error processing batch: {e}")
    finally:
        connection_pool.putconn(conn)
