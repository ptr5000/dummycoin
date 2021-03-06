"""
Transactions

References:

https://bitcoin.org/en/developer-guide#transactions
https://github.com/bitcoinbook/bitcoinbook/blob/second_edition/ch02.asciidoc

"""
from datetime import datetime
from utils import sha1, sign, generate_key
import uuid


class UnauthorizedTxException(Exception):
    """
    Raised when transaction validation fails.
    """
    pass


class TxException(Exception):
    """
    General transaction exception.
    """
    pass


class TxType:
    """
    TxType defines the supported transactions types.

    NORMAL: transaction is a transaction between addresses.
    COINBASE: transaction is a reward from mining.
    """
    NORMAL = 0
    COINBASE = 1


class TxOut:
    """
    Transaction data that carries the output information, i.e. how much is
    spent and who it is transferred to.
    """
    def __init__(self, value, address):
        """
        Initialize TxOut

        Args:
            value: how much we transfer value in this transaction.
            address: to whom we transfer the value.
        """
        self.value = value
        self.address = address

    def get_state(self):
        """
        Returns current state as string.
        """
        return "{}{}".format(self.value, self.address)

    def __str__(self):
        return "out {} => ...{}".format(self.value, self.address[-25:])


class TxIn:
    """
    Transactions that contain the unspent value. I.e. the source where the
    value is transferred from to all the given outputs.
    """
    def __init__(self, prev_outtx, signature, address, value):
        """
        Initialize TxIn

        Args:
            prev_outtx: Id of previous transaction
            signature: Signature for validation
            address: Where this is transferred to
            value: How much value this transaction input contains
        """
        self.prev_outtx = prev_outtx
        self.signature = signature
        self.address = address
        self.value = value

    def get_state(self):
        """
        Returns current state as string.
        """
        return self.prev_outtx

    def __str__(self):
        return "in {}({}) ...{}".format(
            self.prev_outtx, self.value, self.address[-25:])


class Transaction:
    """
    Transaction is a transfer of coin value.
    """
    def __init__(self, priv_key, txtype=TxType.NORMAL):
        """
        Initialise Transaction

        Args:
            priv_key: Private key of the sender
            txtype: TxType i.e. whether this is normal tx or coinbase.
        """
        self.timestamp = datetime.now()
        self.hash = None
        self.priv_key = priv_key
        self.inputs = []
        self.outputs = []
        self.txtype = txtype

        if txtype == TxType.COINBASE:
            self.priv_key = "COINBASE"

    def finalize(self):
        """
        Calculate hash for this transaction when it's done.
        """
        vin = [i.get_state() for i in self.inputs]
        vout = [o.get_state() for o in self.outputs]
        self.hash = sha1("".join(vin).join(vout))

    def add_out(self, value, to_address):
        """
        Add output transaction into this transaction

        Args:
            value: Value of the transaction input
            to_address: To whom the transaction is addressed to.
        """
        self.outputs.append(TxOut(value, to_address))

    def add_in(self, prev_outtx, signature, from_address, value):
        """
        Add input transaction into this transaction.

        Args:
            prev_outtx: Id of previous transaction
            signature: Signature for validation
            address: Where this is transferred to
            value: How much value this transaction input contains
        """
        self.inputs.append(TxIn(prev_outtx, signature, from_address, value))

    def is_coinbase(self):
        """
        Returns whether this is a coinbase (reward) transaction or not.
        """
        return self.txtype == TxType.COINBASE

    def get_ledger(self, address):
        """
        Return outputs and inputs and their value. This can
        be used to calculate balance from unspent transaction
        outputs (utxo) for given address.

        Args:
            address: Address string

        Returns:
            Array of transactions and their hash and value.
        """
        ledger = []

        debit = map(lambda x: {'hash': self.hash, 'value': x.value},
                    filter(lambda x: x.address == address, self.outputs))
        credit = map(lambda x: {'hash': self.hash, 'value': -x.value},
                     filter(lambda x: x.address == address, self.inputs))

        ledger.extend(debit)
        ledger.extend(credit)

        return ledger

    def __str__(self):
        if self.priv_key == "COINBASE":
            out = "  sender: " + str(self.priv_key) + "\n"
        else:
            out = "  sender: ..." + str(self.priv_key.publickey()[-25:]) + "\n"
        out += "  hash: " + self.hash + "\n"
        out += "  timestamp: " + str(self.timestamp) + "\n"

        for i in self.inputs:
            out += "    " + str(i) + "\n"

        for i in self.outputs:
            out += "    " + str(i) + "\n"

        return out
