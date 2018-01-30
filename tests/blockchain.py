
import unittest

from lib.blockchain import Blockchain
from lib.transaction import Transaction, TxType, Transfer
from lib.utils import generate_key, sign, verify_sig

class BlockchainTest(unittest.TestCase):

	def test_pending_transactions(self):
		sender = generate_key()
		receiver = generate_key()

		tx = Transaction(sender, type=TxType.COINBASE)
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
		SENDER_ORIG_VALUE = 10
		SEND_AMOUNT = 5

		blockchain = Blockchain()

		sender = generate_key()
		receiver = generate_key()

		# This is an empty blockchain so create value from thin air.
		tx1 = Transaction(sender, type=TxType.COINBASE)
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
		newb = blockchain.get_new_block()

		self.assertEqual(len(newb.transactions), 3)
		
		for _tx in newb.transactions:
			for input in _tx.inputs:
				self.assertIsNotNone(_tx.hash)
				self.assertIsNotNone(input.signature)
				self.assertTrue(verify_sig(sender, input.signature, _tx.hash))


