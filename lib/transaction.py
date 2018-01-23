"""
Transactions

https://bitcoin.org/en/developer-guide#transactions
"""
from datetime import datetime
from utils import sha1
import uuid

class TxOut:
	def __init__(self, value, target_pubkey):
		self.value = value
		self.target_pubkey = target_pubkey

	def get_state(self):
		return "{}{}".format(self.value, self.target_pubkey)

class TxIn:
	def __init__(prev_outtx, sig):
		self.prev_outtx = prev_outtx
		self.sig = sig

	def get_state(self):
		return self.prev_outtx

class Transaction:
	"""
	Transaction is a transfer of coin value. 
	"""
	inputs = []
	outputs = []
	
	def __init__(self):
		self.timestamp = datetime.now()
		self.hash = None
		
	def finalize(self):
		vin = [i.get_state() for i in self.inputs]
		vout = [o.get_state() for o in self.outputs]
		self.hash = sha1("".join(vin).join(vout))

	def add_out(self, value, target_pubkey):
		self.outputs.append(TxOut(value, target_pubkey))
	
	def add_in(self, prev_outtx, sig):
		self.inputs.append(TxIn(prev_outtx, sig))

	def sign(self, secret_key):
		pass





