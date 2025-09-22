from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from blockchain import Blockchain
from publishersubscriber import PublishSubscribe
from contextlib import asynccontextmanager
import asyncio
import httpx

# Root node address that runs the chain initially for sync
ROOT_ADDRESS = 'http://127.0.0.1:8000'
blockchain = Blockchain()
pubsub = PublishSubscribe(blockchain)

async def sync_chain():
    """
    Sync the local blockchain with the root node's blockchain.
    so that a new node that joins the network starts with the latest chain.
    """
    try:
        # httpx helps in async calling if the port has not yet started. It does not block the start of fastapi app
        async with httpx.AsyncClient() as client:
            req = await client.get(f'{ROOT_ADDRESS}/api/blocks')
        if req.status_code == 200:
            root_chain = req.json().get("chain", [])
            print('SYNCING WITH ROOT CHAIN: ', root_chain)
            blockchain.replace_chain(root_chain)
        else:
            print(f"Error: received status {req.status_code}")
    except Exception as e:
        print(f"Error syncing: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This contains all the calls that should be executed before the app starts running
    """
    await sync_chain()
    # initializes the pub/sub system
    await pubsub.initialize()  
    # runs asyncronously & listens to the channel if anything is broadcasted. If yes, then handles that message
    asyncio.create_task(pubsub.handle_message())
    # broadcasts the current chain on the channel
    await pubsub.broadcast_chain()
    yield

app = FastAPI(lifespan=lifespan)

@app.get('/api/blocks')
async def get_blocks():
    """
    Endpoint API to return the current blockchain.
    Returns:
        json: each block in the chain in json format
    """
    chain_dicts = [block.__dict__ for block in blockchain.chain]
    return JSONResponse(content={"chain": chain_dicts})

@app.post('/api/mineblock')
async def mine_block(request: dict = Body(...)):
    """
    Endpoint to mine a block. Any node which is part of the network can mine a block.
    After mining, broadcasts the chain to everyone who has subscribed
    Returns:
        json: updated chain in json format 
    """
    data = request.get("data", "")
    blockchain.add_block(data)
    await pubsub.broadcast_chain()
    chain_dicts = [block.__dict__ for block in blockchain.chain]
    return JSONResponse(content={"chain": chain_dicts})
