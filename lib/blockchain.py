
from utils import sha1, verify_sig
from transaction import UnauthorizedTxException, TxException
from datetime import datetime

MINING_REWARD = 10

class Block:
    def __init__(self, prev):
        self.prev = prev
        self.transactions = []
        self.nonce = None
        self.index = 0
        self.hash = None
        self.difficulty = 1
        self.timestamp = None
        
        # This is the genesis block.
        if prev is None:
            self.finalize() 

    def finalize(self):
        self.timestamp = datetime.now()

        txdata = map(lambda x:x.hash, self.transactions) 
        self.hash = sha1("{}{}{}{}"
            .format(self.prev, self.index, self.nonce, self.timestamp)
            .join(txdata))

    def add_transaction(self, transaction):
        transactions.append(transaction)

    def get_transactions(self, address):
        return reduce(list.__add__, map(lambda x:x.get_ledger(address), self.transactions), [])
        
class Blockchain:
    def __init__(self):
        self.chain = [Block(None)]
        self.pending_tx = []

    def add(self, transaction):
        """
        Add new transaction to blockchain mining queue. 
        """
        transaction.finalize()

        if not self.verify(transaction):
            raise UnauthorizedTxException()

        self.pending_tx.append(transaction)
    
    def get_pending_transactions(self):
        """
        Return the list of pending (unapproved) transactions.
        """
        return self.pending_tx

    def verify(self, transaction):
        """
        Verify the authenticity of the transaction. 
        """
        if not transaction:
            raise TypeError

        if not transaction.hash:
            raise TxException("Transaction hash is empty")
        
        if not transaction.priv_key:
            raise TxException("Private key is missing")
    
        for input in transaction.inputs:
            if input.signature == None:
                raise TxException("Input signature is empty")
            
            if not verify_sig(transaction.priv_key, input.signature, input.prev_outtx):
                return False

        return True

    def scan_unspent_transactions(self, address):
        """
        Scan all the transactions from the blockchain and pending transactions by
        given owner address. 
        """
        utxo = map(lambda x:x.get_transactions(address), self.chain)
        utxo.extend(map(lambda x:x.get_ledger(address), self.pending_tx))
        return reduce(list.__add__, utxo)

    def get_genesis_block(self):
        """
        Return the genesis block.
        """
        return self.chain[0]

    def top(self):
        return self.chain[-1]
    
    def add_block(self, block):
        """
        Add new block to blockchain
        """
        top = self.chain[-1]
        if block.index == top.index + 1 and block.prev == top.hash:

            # TODO: also validate mined hash
            self.chain.append(block)
            
            # Remove transactions that were added within the block from pending tx list.
            obsoletes = map(lambda x: x.hash, block.transactions)
            self.pending_tx = [tx for tx in self.pending_tx if tx.hash not in obsoletes]
            
    



    