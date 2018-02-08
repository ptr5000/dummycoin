
import unittest

from lib.base64 import Base64

class Base64Test(unittest.TestCase):

    def test_vectors(self):
        b64 = Base64()

        self.assertEqual(b64.encode(""), "")
        self.assertEqual(b64.encode("f"), "Zg==")
        self.assertEqual(b64.encode("fo"), "Zm8=")
        self.assertEqual(b64.encode("foo"), "Zm9v")
        self.assertEqual(b64.encode("foob"), "Zm9vYg==")
        self.assertEqual(b64.encode("fooba"), "Zm9vYmE=")
        self.assertEqual(b64.encode("foobar"), "Zm9vYmFy")
   