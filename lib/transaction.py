"""
Transactions

References:

https://bitcoin.org/en/developer-guide#transactions
http://chimera.labs.oreilly.com/books/1234000001802/ch02.html#_bitcoin_transactions

"""
from datetime import datetime
from utils import sha1, sign
import uuid

class TxOut:
	def __init__(self, value, target_pubkey):
		self.value = value
		self.target_pubkey = target_pubkey

	def get_state(self):
		return "{}{}".format(self.value, self.target_pubkey)

class TxIn:
	signature = None

	def __init__(self, prev_outtx):
		self.prev_outtx = prev_outtx
		
	def get_state(self):
		return self.prev_outtx

class Transaction:
	"""
	Transaction is a transfer of coin value. 
	"""
	
	def __init__(self, priv_key):
		self.timestamp = datetime.now()
		self.hash = None
		self.priv_key = priv_key
		self.inputs = []
		self.outputs = []
		
	def finalize(self):
		vin = [i.get_state() for i in self.inputs]
		vout = [o.get_state() for o in self.outputs]
		
		self.hash = sha1("".join(vin).join(vout))
		
		signature = sign(self.priv_key, self.hash)
		
		for input in self.inputs:
			input.signature = signature

	def add_out(self, value, target_pubkey):
		self.outputs.append(TxOut(value, target_pubkey))
	
	def add_in(self, prev_outtx):
		_txIn = TxIn(prev_outtx)
		self.inputs.append(_txIn)
	
	def __unicode(self):
		return self.hash

	

		





