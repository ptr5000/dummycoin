
from utils import sha1, verify_sig
from transaction import UnauthorizedTxException, TxException
from datetime import datetime

MINING_REWARD = 10


class Block:
    def __init__(self, prev):
        """
        Initialize block.

        Args:
            prev: Previous block id.
        """
        self.prev = prev
        self.transactions = []
        self.nonce = None
        self.index = 0
        self.hash = None
        self.difficulty = 1
        self.timestamp = None

        # This is the genesis block.
        if prev is None:
            self.finalize()

    def finalize(self):
        """
        Set timestamp and calculate the hash for this block. This should
        be called when block is ready to be checked against mining algorithm.
        """
        self.timestamp = datetime.now()

        txdata = map(lambda x: x.hash, self.transactions)
        self.hash = sha1("" + str(self.prev) + str(self.index) +
                         str(self.nonce) + "".join(txdata))

    def get_transactions(self, address):
        """
        Return transactions with given address.

        Args:
            address: public key of address

        Returns:
            List of transactions where given address
            is involved.
        """
        return reduce(list.__add__,
                      map(lambda x: x.get_ledger(address),
                          self.transactions), [])

    def __str__(self):
        out = "BLOCK: " + str(self.index) + "\n"
        out += "Nonce: " + str(self.nonce) + "\n"
        out += "Timestamp: " + str(self.timestamp) + "\n"

        for i in self.transactions:
            out += str(i) + "\n"

        return out


class Blockchain:
    def __init__(self):
        self.chain = [Block(None)]
        self.pending_tx = []

    def add(self, transaction):
        """
        Add new transaction to blockchain mining queue.

        Args:
            transaction: Transaction object.
        """
        transaction.finalize()

        if not self.verify(transaction):
            raise UnauthorizedTxException()

        self.pending_tx.append(transaction)

    def get_pending_transactions(self):
        """
        Return the list of pending (unapproved) transactions.
        """
        return self.pending_tx

    def verify(self, transaction):
        """
        Verify the authenticity of the transaction.

        Args:
            transaction: Transaction object
        """
        if not transaction:
            raise TypeError

        if not transaction.hash:
            raise TxException("Transaction hash is empty")

        if not transaction.priv_key:
            raise TxException("Private key is missing")

        for input in transaction.inputs:
            if input.address != transaction.priv_key.publickey():
                return False

            if input.signature is None:
                raise TxException("Input signature is empty")

            if input.signature == "COINBASE":
                continue

            if not verify_sig(transaction.priv_key,
                              input.signature,
                              input.prev_outtx):
                return False

        return True

    def scan_unspent_transactions(self, address):
        """
        Scan all the transactions from the blockchain and pending
        transactions by given owner address.

        Args:
            address: public key as string
        """
        utxo = map(lambda x: x.get_transactions(address),
                   self.chain)
        utxo.extend(map(lambda x: x.get_ledger(address),
                    self.pending_tx))
        return reduce(list.__add__, utxo, [])

    def get_genesis_block(self):
        """
        Return the genesis block.

        Returns:
            Block object
        """
        return self.chain[0]

    def top(self):
        return self.chain[-1]

    def add_block(self, block):
        """
        Add new block to blockchain

        Args:
            block: Block object
        """
        top = self.chain[-1]
        if block.index == top.index + 1 and block.prev == top.hash:

            # TODO: also validate mined hash
            self.chain.append(block)

            # Remove transactions that were added
            # within the block from pending tx list.
            obsoletes = map(lambda x: x.hash, block.transactions)
            self.pending_tx = [
                tx for tx in self.pending_tx if tx.hash not in obsoletes]
