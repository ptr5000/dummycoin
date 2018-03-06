import json
import unittest
import time

from node.handler import (create_wallet,
                          wallet_info,
                          wallet_send,
                          blockchain,
                          mine)

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
        self.assertEqual(data.get('successful', None), False)

    def test_whole_shebang(self):
        keys = json.loads(create_wallet(None))

        mine(json.dumps({"reward_address": keys.get("public_key")}))

        time.sleep(1)

        wallet_info_data = json.loads(wallet_info(
            json.dumps({"public_key": keys.get("public_key")})))
        self.assertEquals(wallet_info_data.get('balance'), 10)

        receiver_keys = json.loads(create_wallet(None))

        data = {"public_key": keys.get("public_key"),
                "private_key": keys.get("private_key"),
                "amount": 10,
                "recipient": receiver_keys.get("public_key")}

        resp = json.loads(wallet_send(json.dumps(data)))
        self.assertEqual(resp.get('successful', None), True)

        wallet_info_data = json.loads(wallet_info(
            json.dumps({"public_key": keys.get("public_key")})))
        self.assertEquals(wallet_info_data.get('balance'), 0)

        recv_wallet_info_data = json.loads(wallet_info(
            json.dumps({"public_key": receiver_keys.get("public_key")})))
        self.assertEquals(recv_wallet_info_data.get('balance'), 10)
