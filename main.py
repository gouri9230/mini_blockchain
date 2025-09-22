from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from blockchain import Blockchain
from publishersubscriber import PublishSubscribe
from contextlib import asynccontextmanager
import asyncio
import httpx

ROOT_ADDRESS = 'http://127.0.0.1:8000'
blockchain = Blockchain()
pubsub = PublishSubscribe(blockchain)

async def sync_chain():
    try:
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
    await sync_chain()
    await pubsub.initialize()
    asyncio.create_task(pubsub.handle_message())
    await pubsub.broadcast_chain()
    yield

app = FastAPI(lifespan=lifespan)

@app.get('/api/blocks')
async def get_blocks():
    chain_dicts = [block.__dict__ for block in blockchain.chain]
    return JSONResponse(content={"chain": chain_dicts})

@app.post('/api/mineblock')
async def mine_block(request: dict = Body(...)):
    data = request.get("data", "")
    blockchain.add_block(data)
    await pubsub.broadcast_chain()
    chain_dicts = [block.__dict__ for block in blockchain.chain]
    return JSONResponse(content={"chain": chain_dicts})
