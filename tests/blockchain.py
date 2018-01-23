
import unittest

from lib.blockchain import Blockchain
from lib.transaction import Transaction
from lib.utils import generate_key, sign, verify_sig

class BlockchainTest(unittest.TestCase):

	def test_pending_transactions(self):
		key = generate_key()

		tx = Transaction()
		tx.add_out(10, key.publickey())

		blockchain = Blockchain()
		blockchain.add(tx)

		pending_tx = blockchain.get_pending_transactions()

		self.assertEqual(len(filter(lambda x: tx.hash, pending_tx)), 1)

		newb = blockchain.get_new_block()

		pending_tx = blockchain.get_pending_transactions()

		self.assertEqual(len(filter(lambda x: tx.hash, pending_tx)), 0)
		self.assertEqual(len(filter(lambda x: tx.hash, newb.transactions)), 1)






