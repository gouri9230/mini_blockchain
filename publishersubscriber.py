import redis.asyncio as aioredis
import json 

CHANNEL = ["DUMMY", "BLOCKCHAIN"]

class PublishSubscribe():
    def __init__(self, blockchain):
        self.blockchain = blockchain

    async def initialize(self):
        # Creates a Redis client (async).
        self.server = aioredis.Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.server.pubsub()
        # subscribe to the BLOCKCHAIN channel.
        await self.pubsub.subscribe(CHANNEL[1])
        print(f"✅ Subscribed to '{CHANNEL[1]}'. Waiting for messages...")
    
    async def handle_message(self):
        # keeps on listening to the incoming messages on the subscribed channel
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                chain_data = json.loads(message["data"].decode("utf-8"))
                print(f"message received: {chain_data}")
                 # replaces the blockchain if the incoming blockchain is longer than the existing one
                self.blockchain.replace_chain(chain_data)
            

    async def publish_message(self, channel, message):
        if not self.server:
            await self.initialize()
        chain_dicts = [block.__dict__ for block in message.chain]
        # pblishes the chain on the provided channel
        num_subs = await self.server.publish(channel, json.dumps(chain_dicts))
        print(f"number of nodes connected: {num_subs}")

    async def broadcast_chain(self):
        await self.publish_message(channel = CHANNEL[1], message = self.blockchain)
    
