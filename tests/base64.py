
import unittest

from lib.base64 import Base64


class Base64Test(unittest.TestCase):

    def test_vectors_for_encode(self):
        b64 = Base64()

        self.assertEqual(b64.encode(""), "")
        self.assertEqual(b64.encode("f"), "Zg==")
        self.assertEqual(b64.encode("fo"), "Zm8=")
        self.assertEqual(b64.encode("foo"), "Zm9v")
        self.assertEqual(b64.encode("foob"), "Zm9vYg==")
        self.assertEqual(b64.encode("fooba"), "Zm9vYmE=")
        self.assertEqual(b64.encode("foobar"), "Zm9vYmFy")

    def test_vectors_for_decode(self):
        b64 = Base64()
        
        self.assertEqual((""), b64.decode(""))
        self.assertEqual(("f"), b64.decode("Zg=="))
        self.assertEqual(("fo"), b64.decode("Zm8="))
        self.assertEqual(("foo"), b64.decode("Zm9v"))
        self.assertEqual(("foob"), b64.decode("Zm9vYg=="))
        self.assertEqual(("fooba"), b64.decode("Zm9vYmE="))
        
        self.assertEqual(("foobar"), b64.decode("Zm9vYmFy"))
   
