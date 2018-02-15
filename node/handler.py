
from lib.blockchain import Blockchain
from miner import Miner


blockchain = Blockchain()
miner = Miner(blockchain)

def status(query):
    return "OK"

def mine(query):
    if miner.mine(query):
        return "Started mining with reward address:" + query
    else:
        return "Mining already ongoing"