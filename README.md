# A Simple Blockchain in Python

## Overview

A simple blockchain implementation in Python using FastAPI for the API and Redis for node synchronization. This project demonstrates a distributed blockchain with proof-of-work mining, chain validation, and synchronization across multiple nodes.

## Features

- Genesis block initialization
- Implements a blockchain with blocks containing block number, timestamp, data, previous hash, hash, nonce, and difficulty.
- Mines blocks by finding a golden nonce that generates a hash starting with a target number of zeros.
- Validates blockchain with correct cryptographic hash links, difficulty level adjustments
- Uses Redis pub/sub to broadcast the blockchain to connected nodes and sync chain across multiple nodes
- FastAPI endpoints:
  - GET /api/blocks: Get the current blockchain.
  - POST /api/mineblock: Mine a new block.

## Prerequisites

- Python 3.13+
- Redis 6.4.0
- fastapi 0.116.2
- httpx 0.28.1
- requests 2.32.5
- uvicorn 0.36.0

## Installation

1. Clone the Repository
   - https://github.com/gouri9230/mini_blockchain.git
   - cd mini_blockchain

2. Set Up a Virtual Environment
   - python -m venv venv
   - source venv/bin/activate (Linux/Mac)
   - venv\Scripts\activate (Windows)

3. Install Dependencies
   - pip install -r requirements.txt

4. Start Redis Server
   - redis-server

## Usage

1. Run the FastAPI server
   uvicorn main:app (runs in port 8000 by default)
     - at this point you can use GET API on : http://127.0.0.1:8000/api/blocks
     - mine a block using: POST http://127.0.0.1:8000/api/mineblock
     - after mining some blocks, run another server: uvicorn main:app --port 8001
     - you should see the synchronized blockchain with your added blocks on GET API on : http://127.0.0.1:8001/api/blocks
     - mine a block using: POST http://127.0.0.1:8001/api/mineblock and see if it is reflected in the 8000 port server.

## Project Structure
```
├── main.py # FastAPI server and endpoints
├── blockchain.py # Blockchain class managing the chain
├── block.py # Block class and mining logic
├── publishersubscriber.py# Redis Pub/Sub implementation
├── hash_generator.py # Hash function utility
└── README.md # Project documentation
```

## How it works

- Blockchain: Starts with a genesis block. New blocks are mined using proof-of-work, requiring a hash with a target number of leading zeros.
- Mining: The mine_block function adds data to a new block, incrementing the nonce until the hash meets the difficulty target.
- Synchronization: On startup, nodes fetch the chain from the root node (http://127.0.0.1:8000/api/blocks). Then, when a block is mined, the updated chain is broadcasted via Redis pub/sub. Nodes replace their chain with a longer, valid chain received via Redis or HTTP.
- Validation: Ensures chain integrity by checking genesis block, hash links, and difficulty constraints.

## Notes

- Make sure Redis server is running
- The root node port:8000 must be running for other nodes to sync
