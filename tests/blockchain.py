
import unittest

from lib.blockchain import Blockchain, MINING_REWARD
from lib.transaction import Transaction, TxType, UnauthorizedTxException
from lib.wallet import Wallet
from lib.utils import generate_key, sign, verify_sig
from node.miner import Miner

class BlockchainTest(unittest.TestCase):

    def test_pending_transactions(self):
        sender = generate_key()
        receiver = generate_key()
       
        tx = Transaction(None, txtype=TxType.COINBASE)
        tx.add_out(10, receiver.publickey())

        blockchain = Blockchain()
        blockchain.add(tx)

        pending_tx = blockchain.get_pending_transactions()

        self.assertEqual(len(filter(lambda x: tx.hash, pending_tx)), 1)

        miner = Miner(blockchain)
        miner.reward_addr = receiver.publickey()
        newb = miner._mine()
        
        pending_tx = blockchain.get_pending_transactions()

        self.assertEqual(len(filter(lambda x: tx.hash, pending_tx)), 0)
        self.assertEqual(len(filter(lambda x: tx.hash, newb.transactions)), 2)
        
    def test_value_transfer(self):
        """
        Test successful transaction
        """
        SENDER_ORIG_VALUE = MINING_REWARD # Mining reward
        SEND_AMOUNT = 5

        blockchain = Blockchain()

        sender = generate_key()
        receiver = generate_key()
        miner_key = generate_key()

        # This is an empty blockchain so create value out of thin air.
        miner = Miner(blockchain)
        miner.reward_addr = sender.publickey()
        emptyblock = miner._mine()

        self.assertEqual(len(emptyblock.transactions), 1)
    
        # First test with unconfirmed transactions 
        for i in range(1,3):
            wallet = Wallet(sender, blockchain)
            wallet.send(SEND_AMOUNT, receiver.publickey())

            # Scan the blockchain for the transaction that just happened.
            receiver_owns = blockchain.scan_unspent_transactions(receiver.publickey())
            value_received = sum(map(lambda x:x.get('value', 0), receiver_owns))
            self.assertEqual(value_received, SEND_AMOUNT*i)

            sender_owns = blockchain.scan_unspent_transactions(sender.publickey())
            value_owned_by_sender = sum(map(lambda x:x.get('value', 0), sender_owns))
            self.assertEqual(value_owned_by_sender, SENDER_ORIG_VALUE - SEND_AMOUNT*i)


        # Mine the transactions         
        miner = Miner(blockchain)
        miner.reward_addr = miner_key.publickey()
        newb = miner._mine()

        # Test with confirmed transactions
        receiver_owns = blockchain.scan_unspent_transactions(receiver.publickey())
        value_received = sum(map(lambda x:x.get('value', 0), receiver_owns))
        self.assertEqual(value_received, SEND_AMOUNT*2) 

        sender_owns = blockchain.scan_unspent_transactions(sender.publickey())
        value_owned_by_sender = sum(map(lambda x:x.get('value', 0), sender_owns))
        self.assertEqual(value_owned_by_sender, SENDER_ORIG_VALUE - SEND_AMOUNT*2) 

        # Check whether miner received the award
        miner_owns = blockchain.scan_unspent_transactions(miner_key.publickey())
        value_owned_by_miner = sum(map(lambda x:x.get('value', 0), miner_owns))
        self.assertEqual(value_owned_by_miner, MINING_REWARD)

        self.assertEqual(len(newb.transactions), 3)
    
    
    def _test_fraudulent_tx(self, victim, blockchain):
        """
        Try transaction from somebody else's "wallet"
        """
        
        miner_key = generate_key()
        perpetrator = generate_key()
        
        utxo = blockchain.scan_unspent_transactions(victim.publickey())
        
        perpetrator_owns = blockchain.scan_unspent_transactions(perpetrator.publickey())
        self.assertEqual(len(perpetrator_owns), 0) # Sanity check

        # Let's handcraft tx that tries to steal victim's coins. 		
        tx = Transaction(perpetrator) # Sign it with random key
        
        utxo = blockchain.scan_unspent_transactions(victim.publickey()) # Get victim's utxo
        
        debit = sum(map(lambda x:x['value'], utxo))

        for credit in utxo:
            tx.add_in(credit['hash'], sign(perpetrator, credit['hash']), victim.publickey(), credit['value'])

        tx.add_out(debit, perpetrator.publickey())

        try:
            blockchain.add(tx)
            self.fail("Should've thrown UnauthorizedTxException")
        except UnauthorizedTxException:
            pass

        miner = Miner(blockchain)
        miner.reward_addr = miner_key.publickey()
        minedblock = miner._mine()

        perpetrator_owns = blockchain.scan_unspent_transactions(perpetrator.publickey())

        self.assertEqual(len(perpetrator_owns), 0) # Should own nothing. This tx should've failed. 

    def test_fraudulent_tx_source_coinbase(self):
        blockchain = Blockchain()

        victim = generate_key()
        miner = Miner(blockchain)
        miner.reward_addr = victim.publickey()
        emptyblock = miner._mine()
        self.assertEqual(len(emptyblock.transactions), 1)
        self._test_fraudulent_tx(victim, blockchain)
    
    def test_fraudulent_tx_source_other_user(self):
        blockchain = Blockchain()

        victim = generate_key()
        miner_key = generate_key()

        miner = Miner(blockchain)
        miner.reward_addr = miner_key.publickey()
        emptyblock = miner._mine()

        transfer = Wallet(miner_key, blockchain)
        transfer.send(10, victim.publickey())
        
        self.assertEqual(len(emptyblock.transactions), 1)
        self._test_fraudulent_tx(victim, blockchain)
    
        
    def test_chained_tx(self):
        blockchain = Blockchain()

        member1 = generate_key()
        member2 = generate_key()
        member3 = generate_key()

        miner = Miner(blockchain)
        miner.reward_addr = member1.publickey()
        emptyblock = miner._mine()

        wallet1 = Wallet(member1, blockchain)
        wallet1.send(10, member2.publickey())
    
        wallet2 = Wallet(member2, blockchain)
        wallet2.send(10, member3.publickey())

        wallet3 = Wallet(member3, blockchain)
        
        self.assertEqual(wallet1.balance(), 0)
        self.assertEqual(wallet2.balance(), 0)
        self.assertEqual(wallet3.balance(), 10)
        
        







