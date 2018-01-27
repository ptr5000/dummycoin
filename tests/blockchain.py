
import unittest

from lib.blockchain import Blockchain
from lib.transaction import Transaction
from lib.utils import generate_key, sign, verify_sig

class BlockchainTest(unittest.TestCase):

	def test_pending_transactions(self):
		sender = generate_key()
		receiver = generate_key()

		tx = Transaction(sender)
		tx.add_out(10, receiver.publickey())

		blockchain = Blockchain()
		blockchain.add(tx)

		pending_tx = blockchain.get_pending_transactions()

		self.assertEqual(len(filter(lambda x: tx.hash, pending_tx)), 1)

		newb = blockchain.get_new_block()

		pending_tx = blockchain.get_pending_transactions()

		self.assertEqual(len(filter(lambda x: tx.hash, pending_tx)), 0)
		self.assertEqual(len(filter(lambda x: tx.hash, newb.transactions)), 1)
		
	def test_value_transfer(self):
		blockchain = Blockchain()

		sender = generate_key()
		receiver = generate_key()

		# This is an empty blockchain so create value from thin air.
		
		tx1 = Transaction(sender)
		tx1.add_out(10, sender.publickey())
		blockchain.add(tx1)
		
		# Sender has now unspent transaction. Spend half of it. 
		tx2 = Transaction(sender)
		tx2.add_in(tx1.hash)
		tx2.add_out(5, receiver.publickey())
		blockchain.add(tx2)

		self.assertEqual(len(blockchain.get_pending_transactions()), 2)

		newb = blockchain.get_new_block()

		self.assertEqual(len(newb.transactions), 2)

		for _tx in newb.transactions:
			for input in _tx.inputs:
				self.assertIsNotNone(_tx.hash)
				self.assertIsNotNone(input.signature)
				self.assertTrue(verify_sig(sender, input.signature, _tx.hash))

		#receiver_owns = blockchain.fetch_transactions(receiver.publickey())
		
		#self.assertEqual(len(receiver_owns), 1)
		

