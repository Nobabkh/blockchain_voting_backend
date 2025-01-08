from blockchain import Blockchain, Vote, Block, Candidate
import datetime

# Step 1: Generate a secret key (do this once and save it securely)
blockchain = Blockchain()
blockchain.add_block(Vote(id=1, voter_id="123", candidate_id="456", state=[Candidate.create(id="456", vote_count=0, time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), Candidate.create(id="457", vote_count=5, time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))]))
newblock = blockchain.get_latest_block()
print(newblock.data)
data = blockchain.get_block_data(newblock)
print(data)