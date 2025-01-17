from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import requests
from blockchain import Blockchain, Vote, Block, Candidate, VoteRequest
import datetime
from collections import defaultdict

app = FastAPI()

origins = [
    "http://localhost:80",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)
blockchain = Blockchain()

class NodeAddress(BaseModel):
    address: str

class ChainData(BaseModel):
    chain: List[dict]
    length: int

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
async def new_vote(vote: VoteRequest):
    v: Vote = blockchain.get_block_data(blockchain.get_latest_block())
    if v ==None:
        blockchain.add_vote(Vote(id=1, voter_id=vote.voter_id, candidate_id=vote.candidate_id, state=[Candidate(id=vote.candidate_id, vote_count=1, time=datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))]))
        return {"message": "Vote will be added to the next mined block"}
    
    
    if vote.candidate_id not in [v1.id for v1 in v.state]:
        v.state.append(Candidate(id=vote.candidate_id, vote_count=1, time=datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
        newv = Vote(id=v.id+1, voter_id=vote.voter_id, candidate_id=vote.candidate_id, state=v.state)
        blockchain.add_vote(newv)
        return {"message": "Vote will be added to the next mined block"}
    else:
        i = 0
        for vi in v.state:
            if vi.id == vote.candidate_id:
                v.state[i] = Candidate(id=v.state[i].id, vote_count=v.state[i].vote_count+1, time=datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
                break
            i += 1
        
        blockchain.add_vote(Vote(id=v.id+1, voter_id=vote.voter_id, candidate_id=vote.candidate_id, state=v.state))
    return {"message": "Vote will be added to the next mined block"}

@app.get("/mine")
async def mine():
    new_blocks = blockchain.mine_block()
    if not new_blocks:
        raise HTTPException(status_code=400, detail="No votes to mine")
    # new_blocks = new_blocks[1: len(new_blocks)-1]
    if len(new_blocks) == 0:
        return {"message": "No new votes to mine"}
    return [{
        "message": "New block forged",
        "index": new_block.index,
        "transactions": blockchain.get_block_data(new_block),
        "hash": new_block.hash
    } for new_block in new_blocks]

@app.get("/nodes/resolve")
async def consensus():
    replaced = await resolve_conflicts()
    if replaced:
        return {"message": "Our chain was replaced", "new_chain": blockchain.chain}
    return {"message": "Our chain is authoritative", "chain": blockchain.chain}

@app.get('/validate-chain')
async def validate_chain():
    return {"is_valid": blockchain.is_chain_valid()}

async def resolve_conflicts():
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



@app.get("/votes/count")
async def count_votes():
    vote_count = defaultdict(int)
    
    vote: Vote = blockchain.get_block_data(blockchain.get_latest_block())
    if vote ==None:
        return None
    
    return vote.state


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)