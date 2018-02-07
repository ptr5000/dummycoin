from transaction import Transaction

class InsufficientFundsException(Exception):
    pass

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
            tx.add_in(credit['hash'], credit['signature'], self.sender_key.publickey(), credit['value'])

        tx.add_out(self.amount, self.to_addr)
        tx.add_out(change, self.sender_key.publickey())

        self.blockchain.add(tx)
    
