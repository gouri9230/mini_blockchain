import redis

CHANNEL = ["DUMMY", "BLOCKCHAIN"]

def publish():
    publisher = redis.Redis(host='localhost', port=6379, db=0)
    num_sub = publisher.publish(CHANNEL[1], "hey there")
    print(f'number of subscribers: {num_sub}')
