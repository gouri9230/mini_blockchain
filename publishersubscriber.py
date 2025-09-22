import redis.asyncio as aioredis
import json 

CHANNEL = ["DUMMY", "BLOCKCHAIN"]

class PublishSubscribe():
    def __init__(self, blockchain):
        self.blockchain = blockchain

    async def initialize(self):
        self.server = aioredis.Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.server.pubsub()
        await self.pubsub.subscribe(CHANNEL[1])
        print(f"✅ Subscribed to '{CHANNEL[1]}'. Waiting for messages...")
    
    async def handle_message(self):
        async for message in self.pubsub.listen():
            print("message: ", message)
            if message["type"] == "message":
                chain_data = json.loads(message["data"].decode("utf-8"))
                print(f"message received: {chain_data}")
                self.blockchain.replace_chain(chain_data)
            

    async def publish_message(self, channel, message):
        if not self.server:
            await self.initialize()
        print("message chain is: ", message.chain)
        chain_dicts = [block.__dict__ for block in message.chain]
        num_subs = await self.server.publish(channel, json.dumps(chain_dicts))
        print(f"number of nodes connected: {num_subs}")

    async def broadcast_chain(self):
        await self.publish_message(channel = CHANNEL[1], message = self.blockchain)
    
