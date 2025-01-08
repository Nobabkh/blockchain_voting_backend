import hashlib
import time
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import datetime
from cryptography.fernet import Fernet
import json

from pydantic import BaseModel
from pydantic import BaseModel
from constant.secret.ApplicationKey import ENCRYPT_KEY
class Candidate(BaseModel):
    id: str
    vote_count: int
    time: str
    
    @classmethod
    def create(cls, id: str, vote_count: int, time: str) -> "Candidate":
        return cls(id=id, vote_count=vote_count, time=time)
    
    class Config:
        orm_mode = True

class Vote(BaseModel):
    id: int
    voter_id: str
    candidate_id: str
    state: list[Candidate]
    
    @classmethod
    def create(cls, id: int, voter_id: str, candidate_id: str, state: list[Candidate]) -> "Vote":
        return cls(id=id, voter_id=voter_id, candidate_id=candidate_id, state=state)
    
    class Config:
        orm_mode = True


class Block:
    
    def __init__(self, index: int, timestamp: datetime.datetime, data: str, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    fernet = Fernet(ENCRYPT_KEY)
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.fernet = Fernet(ENCRYPT_KEY)

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        return Block(0, str(datetime.datetime.now()), "Genesis Block", "0")

    def get_latest_block(self):
        """Return the latest block in the chain."""
        return self.chain[-1]

    def add_block(self, vote: Vote):
        """Add a new block to the chain."""
        latest_block = self.get_latest_block()
        
        
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=str(datetime.datetime.now()),
            data=self.fernet.encrypt(json.dumps(vote.model_dump()).encode("utf-8")),
            previous_hash=latest_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Check if the blockchain is valid."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if the current block's previous hash matches the previous block's hash
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_block_data(self, block: Block):
        """Find a block by its name."""
        data = json.loads(self.fernet.decrypt(block.data).decode("utf-8"))
        return Vote(**data)

# Flask App for Voting System

'''
app = Flask(__name__)
socketio = SocketIO(app)
blockchain = Blockchain()
peers = set()

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    voter_id = data.get('voter_id')
    candidate = data.get('candidate')

    if not voter_id or not candidate:
        return jsonify({'message': 'Invalid vote'}), 400

    blockchain.add_vote(voter_id, candidate)
    return jsonify({'message': 'Vote added successfully'}), 201

@app.route('/mine', methods=['GET'])
def mine():
    new_block = blockchain.mine_block()
    if not new_block:
        return jsonify({'message': 'No votes to mine'}), 400

    emit_new_block(new_block)
    return jsonify({
        'message': 'Block mined successfully',
        'block': {
            'index': new_block.index,
            'timestamp': new_block.timestamp,
            'votes': new_block.votes,
            'hash': new_block.hash,
            'previous_hash': new_block.previous_hash
        }
    }), 201

@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = [{
        'index': block.index,
        'timestamp': block.timestamp,
        'votes': block.votes,
        'hash': block.hash,
        'previous_hash': block.previous_hash
    } for block in blockchain.chain]
    return jsonify({'chain': chain_data, 'length': len(blockchain.chain)}), 200

@app.route('/register_node', methods=['POST'])
def register_node():
    node_address = request.json.get('address')
    if not node_address:
        return jsonify({'message': 'Invalid node address'}), 400

    peers.add(node_address)
    return jsonify({'message': 'Node registered successfully'}), 201

@app.route('/sync_chain', methods=['GET'])
def sync_chain():
    global blockchain
    longest_chain = None
    max_length = len(blockchain.chain)

    for peer in peers:
        try:
            response = requests.get(f'http://{peer}/get_chain')
            if response.status_code == 200:
                peer_chain = response.json()['chain']
                peer_length = response.json()['length']

                if peer_length > max_length and blockchain.is_chain_valid(peer_chain):
                    max_length = peer_length
                    longest_chain = peer_chain
        except Exception as e:
            print(f"Error syncing with peer {peer}: {e}")

    if longest_chain:
        blockchain.chain = longest_chain
        return jsonify({'message': 'Chain updated'}), 200

    return jsonify({'message': 'No updates found'}), 200

def emit_new_block(block):
    for peer in peers:
        try:
            requests.post(f'http://{peer}/add_block', json={
                'index': block.index,
                'timestamp': block.timestamp,
                'votes': block.votes,
                'previous_hash': block.previous_hash,
                'hash': block.hash
            })
        except Exception as e:
            print(f"Error broadcasting to peer {peer}: {e}")

if __name__ == '__main__':
    app.run(port=5000)
'''