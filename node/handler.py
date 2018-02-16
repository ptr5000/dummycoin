
import json
from lib.blockchain import Blockchain
from lib.wallet import Wallet, InsufficientFundsException
from lib.utils import generate_key
from lib.rsa import RSAKey, RSAPublicKey, RSAPrivateKey
from miner import Miner


blockchain = Blockchain()
miner = Miner(blockchain)


def status(query):
    return "OK"

def mine(data):
    l = json.loads(data)

    if miner.mine(l.get('reward_address')):
        return "Started mining with reward address:" + l.get('reward_address')
    else:
        return "Mining already ongoing"

def create_wallet(data):
    key = generate_key()

    return json.dumps({"public_key": str(key.publickey()),
                       "private_key": str(key.privatekey())})


def wallet_info(data):
    l = json.loads(data)

    key = RSAKey(RSAPublicKey.load(l.get('public_key')), None)
    
    wallet = Wallet(key, blockchain)
    
    return json.dumps({"balance": wallet.balance()})


def wallet_send(data):
    l = json.loads(data)
    
    key = RSAKey(RSAPublicKey.load(l.get('public_key')), RSAPrivateKey.load(l.get('private_key')))
    
    wallet = Wallet(key, blockchain)
    try:
        wallet.send(l.get('amount'), l.get('recipient'))
    except InsufficientFundsException:
        return json.dumps({"successful": False, "message": "Insufficient funds"})
    
    return json.dumps({"successful": True})
    
