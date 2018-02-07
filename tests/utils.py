
import unittest

from lib.utils import generate_key, sign, verify_sig

class UtilsTest(unittest.TestCase):
    def test_rsa(self):
        test_hash = "1234"

        key = generate_key()

        signature = sign(key, test_hash)

        self.assertTrue(verify_sig(key, signature, test_hash))
        self.assertFalse(verify_sig(key, signature, "4321"))
        self.assertFalse(verify_sig(key, signature, "12345"))
