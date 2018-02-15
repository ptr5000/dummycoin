
from lib.blockchain import Block, Blockchain, MINING_REWARD
from lib.transaction import Transaction, TxType

class Miner:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.running = False

    def create_new_block(self):
        """
        Create a fresh new block that contains all valid
        pending transactions. 
        """
        newb = Block(self.blockchain.top().hash)
        newb.index = self.blockchain.top().index + 1

        newb.transactions.extend(self.blockchain.get_pending_transactions())
            
        tx = Transaction(None, txtype=TxType.COINBASE)
        tx.add_out(MINING_REWARD, self.reward_addr)
        tx.finalize()

        newb.transactions.append(tx)

        return newb

    def check_hash(self, block):
        hashint = int(block.hash, 16)

        for i in range(block.difficulty):
            if hashint & 1 != 0:
                return False
            hashint >>= 1
         
        return True

    def mine(self, reward_addr):
        if self.running:
            return False

        self.reward_addr = reward_addr
        
        thread = Thread(target=self._mine)
        thread.start()

        return True
    
    def stop(self):
        self.running = False
    
    def _mine(self):
        self.running = True

        block = self.create_new_block()
        block.nonce = 1

        while self.running:
            
            block.finalize()
            #print "Trying with ", block.nonce, block.hash
            if self.check_hash(block):
                break

            block.nonce+=1
        
        self.blockchain.add_block(block)

        return block


        
