
import unittest

from lib.utils import generate_key, sign, verify_sig
from lib.rsa import RSAPublicKey, RSAPrivateKey


class UtilsTest(unittest.TestCase):
    def test_rsa(self):
        test_hash = "1234"

        key = generate_key()

        signature = sign(key, test_hash)

        self.assertTrue(verify_sig(key, signature, test_hash))
        self.assertFalse(verify_sig(key, signature, "4321"))
        self.assertFalse(verify_sig(key, signature, "12345"))

    def test_format(self):
        key = generate_key()
        keystr = str(key.publickey())
        newkey = RSAPublicKey.load(keystr)

        self.assertEqual(key.public_key.n, newkey.n)
        self.assertEqual(key.public_key.e, newkey.e)

        keystr = str(key.privatekey())
        newkey = RSAPrivateKey.load(keystr)

        self.assertEqual(key.priv_key.n, newkey.n)
        self.assertEqual(key.priv_key.d, newkey.d)
