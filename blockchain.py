import json
from cryptography.fernet import Fernet
import datetime
from typing import List
from pydantic import BaseModel
from constant.secret.ApplicationKey import ENCRYPT_KEY

class Candidate(BaseModel):
    id: str
    vote_count: int
    time: str

    @classmethod
    def create(cls, id: str, vote_count: int, time: str):
        return cls(id=id, vote_count=vote_count, time=time)
    
class VoteRequest(BaseModel):
    candidate_id: str
    voter_id: str

class Vote(BaseModel):
    id: int
    voter_id: str
    candidate_id: str
    state: List[Candidate]

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Implement a proper hashing mechanism here
        return hash(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash))

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_votes = []
        self.fernet = Fernet(ENCRYPT_KEY)
        self.nodes = set()

    def create_genesis_block(self):
        return Block(0, str(datetime.datetime.now()), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, vote: Vote):
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=str(datetime.datetime.now()),
            data=self.fernet.encrypt(json.dumps(vote.model_dump()).encode("utf-8")),
            previous_hash=latest_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    
    def get_votes_by_candidate(self):
        votes_by_candidate = {}
        for block in self.chain:
            for vote in self.get_block_data(block):
                if vote.candidate_id in votes_by_candidate:
                    votes_by_candidate[vote.candidate_id].append(vote)
                else:
                    votes_by_candidate[vote.candidate_id] = [vote]
        return votes_by_candidate

    def get_block_data(self, block: Block):
        if block.index == 0:
            return None
        data = json.loads(self.fernet.decrypt(block.data).decode("utf-8"))
        print(data)
        return Vote(**data)
    
    def get_block_data_0(self, block: Block):
        if block.index == 0:
            return None
        data = json.loads(self.fernet.decrypt(block.data).decode("utf-8"))
        print(data)
        return Vote(**data)

    def add_node(self, address):
        self.nodes.add(address)

    def replace_chain(self, new_chain):
        if len(new_chain) > len(self.chain) and self.is_chain_valid(new_chain):
            self.chain = new_chain
            return True
        return False

    def add_vote(self, vote: Vote):
        self.add_block(vote)
        self.pending_votes.append(vote)

    def mine_block(self):
        if not self.pending_votes:
            return None


        return self.chain