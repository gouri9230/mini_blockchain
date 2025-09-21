# subscriber.py
import redis
from publisher import CHANNEL

def subscribe():
    subscriber = redis.Redis(host='localhost', port=6379, db=0)
    pubsub = subscriber.pubsub()
    pubsub.subscribe(CHANNEL[1])

    print(f"Subscribed to '{CHANNEL[1]}'. Waiting for messages...")

    for message in pubsub.listen():
        print(f"Received message: {message['data']}")



