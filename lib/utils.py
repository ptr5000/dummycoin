
import hashlib
from rsa import RSAKey, RSAPrivateKey, RSAPublicKey


def sha1(s):
    return hashlib.sha1(s).hexdigest()


def generate_key():
    return RSAKey.generate_key()


def sign(key, hash):
    return key.sign(hash)


def verify_sig(key, signature, hash):
    return key.verify(hash, signature)
