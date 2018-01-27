
from utils import sha1

class Block:
	def __init__(self, prev):
		self.prev = prev
		self.transactions = []
		self.nonce = None
		self.index = 0
		self.hash = None
		
		# This is the genesis block.
		if prev is None:
			self.finalize() 

	def finalize(self):
		tx = [i.hash for i in self.transactions]
		self.hash = sha1("{}{}{}"
			.format(self.prev, self.index, self.nonce)
			.join(tx))

	def add_transaction(transaction):
		transactions.append(transaction)

class Blockchain:
	def __init__(self):
		self.chain = [Block(None)]
		self.pending_tx = []

	def add(self, transaction):
		"""
		Add new transaction to blockchain mining queue. 
		"""
		transaction.finalize()
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
		pass

	def fetch_transactions(self, addr):
		"""
		Return all the transactions from the blockchain by
		given owner address. 
		"""
		pass

	def get_genesis_block(self):
		"""
		Return the genesis block.
		"""
		return self.chain[0]

	def get_new_block(self):
		"""
		Generate a fresh new block that contains all valid
		pending transactions. 
		"""
		newb = Block(self.chain[-1].hash)
		newb.index = len(self.chain)

		while len(self.pending_tx) > 0:
			tx = self.pending_tx.pop()
		
			# TODO: check for double spending etc.
			newb.transactions.append(tx)
		
		newb.finalize()

		return newb



	