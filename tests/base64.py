
import unittest

from lib.base64 import base64

class Base64Test(unittest.TestCase):

    def test_vectors(self):
        self.assertEqual(base64(""), "")
        self.assertEqual(base64("f"), "Zg==")
        self.assertEqual(base64("fo"), "Zm8=")
        self.assertEqual(base64("foo"), "Zm9v")
        self.assertEqual(base64("foob"), "Zm9vYg==")
        self.assertEqual(base64("fooba"), "Zm9vYmE=")
        self.assertEqual(base64("foobar"), "Zm9vYmFy")
   