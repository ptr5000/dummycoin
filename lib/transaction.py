"""
Transactions

References:

https://bitcoin.org/en/developer-guide#transactions
https://github.com/bitcoinbook/bitcoinbook/blob/second_edition/ch02.asciidoc

"""
from datetime import datetime
from utils import sha1, sign
import uuid

class InsufficientFundsException(Exception):
	pass

class TxType:
	NORMAL = 0
	COINBASE = 1

class TxOut:
	def __init__(self, value, address):
		self.value = value
		self.address = address

	def get_state(self):
		return "{}{}".format(self.value, self.address)

class TxIn:
	def __init__(self, prev_outtx, address, value):
		self.prev_outtx = prev_outtx
		self.signature = None
		self.address = address
		self.value = value

	def get_state(self):
		return self.prev_outtx

class Transaction:
	"""
	Transaction is a transfer of coin value. 
	"""
	def __init__(self, priv_key, type=TxType.NORMAL):
		self.timestamp = datetime.now()
		self.hash = None
		self.priv_key = priv_key
		self.inputs = []
		self.outputs = []
		self.type = type
		
	def finalize(self):
		vin = [i.get_state() for i in self.inputs]
		vout = [o.get_state() for o in self.outputs]
		
		self.hash = sha1("".join(vin).join(vout))
		
		signature = sign(self.priv_key, self.hash)
		
		for input in self.inputs:
			input.signature = signature

	def add_out(self, value, to_address):
		self.outputs.append(TxOut(value, to_address))
	
	def add_in(self, prev_outtx, from_address, value):
		self.inputs.append(TxIn(prev_outtx, from_address, value))

	def get_ledger(self, address):
		"""
		Return outputs by address.
		"""
		ledger = []

		debit = map(lambda x: {'hash': self.hash, 'value': x.value}, 
				filter(lambda x:x.address == address, self.outputs))
		credit = map(lambda x: {'hash': self.hash, 'value': -x.value}, 
				filter(lambda x:x.address == address, self.inputs))

		ledger.extend(debit)
		ledger.extend(credit)
		
		return ledger
	
	def __unicode__(self):
		return self.hash

class Transfer:
	def __init__(self, amount, sender_key, to_addr, blockchain):
		self.amount = amount
		self.to_addr = to_addr
		self.sender_key = sender_key
		self.blockchain = blockchain
		
	def send(self):
		tx = Transaction(self.sender_key)

		utxo = self.blockchain.scan_unspent_transactions(
				self.sender_key.publickey())
		
		debit = sum(map(lambda x:x['value'], utxo))
		
		change = debit - self.amount

		if change < 0:
			raise InsufficientFundsException()

		for credit in utxo:
			tx.add_in(credit['hash'], self.sender_key.publickey(), credit['value'])

		tx.add_out(self.amount, self.to_addr)
		tx.add_out(change, self.sender_key.publickey())

		self.blockchain.add(tx)
	



	

		





