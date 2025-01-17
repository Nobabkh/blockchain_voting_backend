import argparse
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from blockchain import Blockchain, Vote, Block, Candidate
import socket

def get_local_ip():
    # This function retrieves the local IP address of the device
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Connect to a public DNS server to determine the local IP address
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

def find_server_node(port=8090):
    local_ip = get_local_ip()
    ip_base = local_ip.rsplit('.', 1)[0]
    for i in range(1, 255):
        ip = f"{ip_base}.{i}"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Set a timeout for the connection attempt
            try:
                s.connect((ip, port))
                return f"http://{ip}:{port}"
            except (socket.timeout, ConnectionRefusedError):
                continue
    return None

class NodeAddress(BaseModel):
    address: str

class ChainData(BaseModel):
    chain: List[dict]
    length: int

def create_app():
    app = FastAPI()
    blockchain = Blockchain()

    @app.post("/nodes/register")
    async def register_nodes(node: NodeAddress):
        blockchain.add_node(node.address)
        return {"message": "New node has been added", "total_nodes": list(blockchain.nodes)}

    @app.get("/chain")
    async def get_chain():
        chain_data = [{
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'hash': block.hash,
            'previous_hash': block.previous_hash
        } for block in blockchain.chain]
        return ChainData(chain=chain_data, length=len(blockchain.chain))

    @app.post("/votes/new")
    async def new_vote(vote: Vote):
        blockchain.add_vote(vote)
        return {"message": "Vote will be added to the next mined block"}

    @app.get("/mine")
    async def mine():
        new_block = blockchain.mine_block()
        if not new_block:
            raise HTTPException(status_code=400, detail="No votes to mine")

        return {
            "message": "New block forged",
            "index": new_block.index,
            "transactions": blockchain.get_block_data(new_block),
            "hash": new_block.hash
        }

    @app.get("/nodes/resolve")
    async def consensus():
        replaced = await resolve_conflicts(blockchain)
        if replaced:
            return {"message": "Our chain was replaced", "new_chain": blockchain.chain}
        return {"message": "Our chain is authoritative", "chain": blockchain.chain}

    return app

async def resolve_conflicts(blockchain):
    neighbours = blockchain.nodes
    new_chain = None

    max_length = len(blockchain.chain)

    for node in neighbours:
        response = requests.get(f'http://{node}/chain')

        if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']

            if length > max_length and blockchain.is_chain_valid(chain):
                max_length = length
                new_chain = chain

    if new_chain:
        blockchain.chain = new_chain
        return True

    return False

def register_with_existing_node(new_node_address, existing_node_address):
    data = {"address": new_node_address}
    response = requests.post(f"{existing_node_address}/nodes/register", json=data)
    if response.status_code == 200:
        print(f"Successfully registered with node at {existing_node_address}")
    else:
        print(f"Failed to register with node at {existing_node_address}")

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Run a blockchain node.")
    # parser.add_argument('--port', type=int, default=8000, help='Port to run the node on')
    # parser.add_argument('--register', type=str, help='Address of an existing node to register with')
    # args = parser.parse_args()

    app = create_app()
    node_address = f"http://localhost:8090"

    if args.register:
        register_with_existing_node(node_address, args.register)

    uvicorn.run(app, host="0.0.0.0", port=args.port)