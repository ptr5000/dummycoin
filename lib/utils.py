
import hashlib

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Signature import PKCS1_v1_5 
from Crypto.PublicKey import RSA

def sha1(s):
	return hashlib.sha1(s).hexdigest()

def generate_key():
	rng = Random.new().read
	return RSA.generate(1024, rng)

def sign(key, hash):
	return key.sign(hash, 32)

def verify_sig(key, signature, hash):
	return key.publickey().verify(hash, signature)