from fastapi import FastAPI, Body
from pydantic import BaseModel
from blockchain import Blockchain

app = FastAPI()

blockchain = Blockchain()

@app.get('/api/blocks')
def get_blocks():
    return blockchain.chain

@app.post('/api/mineblock')
def mine_block(request: dict = Body(...)):
    print(request)
    blockchain.add_block(request)
    return {"message": "block mined sucessfully"}