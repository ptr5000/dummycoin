import sys
from math import floor, log

def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        (d,x,y) = egcd(b, a % b)
        return (d, y, x - floor(a/b) * y)
        
def mul_inv(a, b):
    (d,x,y) = egcd(a,b)
    
    if d != 1:
        raise ValueError
    
    return x % b

def mod_exp(a, b, n):
    d = 1
    b = long(b)
  
    while b != 0:
        if b & 1:
            d = (d*a) % n
       
        b >>= 1

        a = (a*a) % n
        
    return d


class RSAPublicKey:
    def __init__(self, e, n):
        self.e = long(e)
        self.n = long(n)

class RSAPrivateKey:
    def __init__(self, d, n):
        self.d = long(d)
        self.n = long(n)

class RSAKey:
    def __init__(self, public_key, priv_key):
        self.public_key = public_key
        self.priv_key = priv_key
        
    @staticmethod
    def generate_key():
        # Randomly selected two prime numbers ;)
        # TODO: primary number generator 
        p = 3967
        q = 7691 
        
        n = p*q

        e = 17  # gcd(17, (p-1)*(q-1)) = 1

        d = long(mul_inv(e, (p-1) * (q-1)))

        print e, n
        print d, n

        # (e,n) public key
        # (d,n) secret key

        return RSAKey(RSAPublicKey(e,n), RSAPrivateKey(d,n))

    def sign(self, hash):
        out = []
        t = []
        for c in hash:
            t.append(ord(c))
            out.append(mod_exp(ord(c), self.priv_key.d, self.priv_key.n))
        
        return out
    
    def verify(self, hash, signature):
        out = []

        for c in signature:
            out.append(chr(mod_exp(c, self.public_key.e, self.public_key.n)))

        return "".join(out) == hash

if __name__ == '__main__':
    #print mod_exp(7, 560000000000000000000000000000000000, 561000000000000000000000000000000000)
    print mod_exp(7, 560, 561)
  
    
    key = RSAKey.generate_key()
  
    ver = key.verify("Jorma", key.sign("Jorma"))

    print ver



        

