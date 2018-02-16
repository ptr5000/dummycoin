from transaction import Transaction

class InsufficientFundsException(Exception):
    pass

class Wallet:
    def __init__(self, key, blockchain):
        self.key = key
        self.blockchain = blockchain
    
    def balance(self):
        """
        Scan unspent transaction outputs (utxo) so we know how much
        balance we've to spent. 
        """
        utxo = self.blockchain.scan_unspent_transactions(
                self.key.publickey())
        
        debit = sum(map(lambda x:x['value'], utxo))
        return debit

    def send(self, amount, to_addr):
        """
        Send money to the given address from this wallet. 
        """
        tx = Transaction(self.key)

        utxo = self.blockchain.scan_unspent_transactions(
                self.key.publickey())
        
        debit = sum(map(lambda x:x['value'], utxo))
        
        change = debit - amount

        if change < 0:
            raise InsufficientFundsException()

        for credit in utxo:
            tx.add_in(credit['hash'], credit['signature'], self.key.publickey(), credit['value'])

        tx.add_out(amount, to_addr)
        tx.add_out(change, self.key.publickey())

        self.blockchain.add(tx)
    
