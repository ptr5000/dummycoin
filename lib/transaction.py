"""
Transactions

References:

https://bitcoin.org/en/developer-guide#transactions
https://github.com/bitcoinbook/bitcoinbook/blob/second_edition/ch02.asciidoc

"""
from datetime import datetime
from utils import sha1, sign
import uuid

class UnauthorizedTxException(Exception):
    pass

class TxException(Exception):
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
    def __init__(self, prev_outtx, signature, address, value):
        self.prev_outtx = prev_outtx
        self.signature = signature
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
        self.signature = None
        
    def finalize(self):
        vin = [i.get_state() for i in self.inputs]
        vout = [o.get_state() for o in self.outputs]
        
        self.hash = sha1("".join(vin).join(vout))
        
        self.signature = sign(self.priv_key, self.hash)
        
        """
        for input in self.inputs:
            input.signature = self.signature
        """

    def add_out(self, value, to_address):
        self.outputs.append(TxOut(value, to_address))
    
    def add_in(self, prev_outtx, signature, from_address, value):
        self.inputs.append(TxIn(prev_outtx, signature, from_address, value))

    def get_ledger(self, address):
        """
        Return outputs by address.
        """
        ledger = []

        debit = map(lambda x: {'hash': self.hash, 'value': x.value, 'signature': self.signature}, 
                filter(lambda x:x.address == address, self.outputs))
        credit = map(lambda x: {'hash': self.hash, 'value': -x.value, 'signature': self.signature}, 
                filter(lambda x:x.address == address, self.inputs))

        ledger.extend(debit)
        ledger.extend(credit)
        
        return ledger
    
    def get_sender(self):
        return self.priv_key
    
    def __unicode__(self):
        return self.hash


    

        





