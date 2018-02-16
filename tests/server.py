import json
import unittest

from node.handler import create_wallet, wallet_info, wallet_send, blockchain
from lib.utils import generate_key

class ServerTest(unittest.TestCase):
    def test_create_wallet(self):
        resp = create_wallet(None)
        data = json.loads(resp)
        self.assertIsNotNone(data.get('public_key', None))
        self.assertIsNotNone(data.get('private_key', None))

    def test_wallet_info(self):
        receiver = generate_key()

        data = {"public_key": str(receiver.publickey())}

        resp = wallet_info(json.dumps(data))
        data = json.loads(resp)
        self.assertIsNotNone(data.get('balance', None))

    def test_wallet_send(self):
        sender = generate_key()
        receiver = generate_key()

        data = {"public_key": str(sender.publickey()),
                "private_key": str(sender.privatekey()),
                "amount": 10,
                "recipient": str(receiver.publickey())}

        resp = wallet_send(json.dumps(data))
        data = json.loads(resp)
        self.assertIsNotNone(data.get('successful', None))

