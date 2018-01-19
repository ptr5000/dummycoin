"""
Transactions

https://bitcoin.org/en/developer-guide#transactions
"""
from datetime import datetime
from utils import sha1
import uuid, pickle

class TxOut:
	def __init__(self, value, target_pub_key):
		self.value = value
		self.target_pub_key = target_pub_key

	def get_state(self):
		return "{}{}".format(self.value, self.target_pub_key)

class TxIn:
	def __init__(prev_out_tx, sig):
		self.prev_out_tx = prev_out_tx
		self.sig = sig

	def get_state(self):
		return self.prev_out_tx

class Transaction:
	"""
	Transaction is a transfer of coin value. 
	"""
	inputs = []
	outputs = []

	def __init__(self):
		self.timestamp = datetime.now()

	def hash(self):
		vin = [i.getState() for i in self.inputs]
		vout = [o.getState() for o in self.outputs]
		return sha1("".join(vin).join(vout))






