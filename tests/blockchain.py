
import unittest

from lib.blockchain import Blockchain
from lib.transaction import Transaction, TxType, UnauthorizedTxException
from lib.wallet import Transfer
from lib.utils import generate_key, sign, verify_sig

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

        newb = blockchain.create_new_block(receiver.publickey())

        blockchain.add_block(newb)
        
        pending_tx = blockchain.get_pending_transactions()

        self.assertEqual(len(filter(lambda x: tx.hash, pending_tx)), 0)
        self.assertEqual(len(filter(lambda x: tx.hash, newb.transactions)), 2)
        
    def test_value_transfer(self):
        """
        Test successful transaction
        """
        SENDER_ORIG_VALUE = 10
        SEND_AMOUNT = 5

        blockchain = Blockchain()

        sender = generate_key()
        receiver = generate_key()

        # This is an empty blockchain so create value out of thin air.
        tx1 = Transaction(sender, txtype=TxType.COINBASE)
        tx1.add_out(SENDER_ORIG_VALUE, sender.publickey())
        blockchain.add(tx1)
        
        for i in range(1,3):
            transfer = Transfer(SEND_AMOUNT, sender, receiver.publickey(), blockchain)
            transfer.send()

            # Scan the blockchain for the transaction that just happened.
            receiver_owns = blockchain.scan_unspent_transactions(receiver.publickey())

            value_received = 0
            for x in receiver_owns:
                value_received += x.get('value', 0)
            self.assertEqual(value_received, SEND_AMOUNT*i)

            sender_owns = blockchain.scan_unspent_transactions(sender.publickey())

            value_owned_by_sender = 0

            for x in sender_owns:
                value_owned_by_sender += x.get('value', 0)

            self.assertEqual(value_owned_by_sender, SENDER_ORIG_VALUE - SEND_AMOUNT*i)

        # Create a new block from these transactions and check that they are valid.
        newb = blockchain.create_new_block(receiver.publickey())

        self.assertEqual(len(newb.transactions), 4)
    

    def test_fraudulent_tx(self):
        """
        Try transaction from somebody else's "wallet"
        """
        blockchain = Blockchain()

        victim = generate_key()
        perpetrator = generate_key()

        # This is an empty blockchain so create value out of thin air.
        victim_tx = Transaction(victim, txtype=TxType.COINBASE)
        victim_tx.add_out(10, victim.publickey())
        blockchain.add(victim_tx)
    
        utxo = blockchain.scan_unspent_transactions(victim.publickey())
        
        perpetrator_owns = blockchain.scan_unspent_transactions(perpetrator.publickey())
        self.assertEqual(len(perpetrator_owns), 0) # Sanity check

        # Let's handcraft tx that tries to steal victim's coins. 		
        tx = Transaction(perpetrator) # Sign it with random key
        
        utxo = blockchain.scan_unspent_transactions(victim.publickey()) # Get victim's utxo
        
        debit = sum(map(lambda x:x['value'], utxo))

        for credit in utxo:
            # TODO: can we forge the signature here? What happens if we do?
            # Does it fail when we mine the block and verify it? 
            tx.add_in(credit['hash'], credit['signature'], victim.publickey(), credit['value'])

        tx.add_out(debit, perpetrator.publickey())

        try:
            blockchain.add(tx)
            self.fail("Should've thrown UnauthorizedTxException")
        except UnauthorizedTxException:
            pass
        
        perpetrator_owns = blockchain.scan_unspent_transactions(perpetrator.publickey())

        self.assertEqual(len(perpetrator_owns), 0) # Should own nothing. This tx should've failed. 

        







