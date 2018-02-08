import sys
from math import floor, log, pow, sqrt
from random import randrange

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

def is_prime(n, s=10):
    """
    Miller-Rabin 
    """
    def witness(a, n):
        u = n - 1
        t = 0

        while u % 2 == 0:
            u >>= 1
            t += 1
        
        x = mod_exp(a, u, n)

        for i in range(0, t):
            xp = x
            x = pow(x, 2) % n
            
            if x == 1 and xp != 1 and xp != n - 1:
                return True
        
        if x != 1:
            return True
        
        return False

    for j in range(0, s):
        a = randrange(1, n-1)

        if witness(a,n):
            return False
        
    return True

def get_random_large_prime():
    while 1:
        a = randrange(100000000000, 90000000000000)

        if is_prime(a):
            break

    print "Found prime: ", a
    return a

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
    def generate_key(e=17):
        rp = False

        # Loop until gcd(e, (p-1)*(q-1)) = 1
        while not rp:
            try:
                p = get_random_large_prime()
                q = get_random_large_prime()
                d = long(mul_inv(e, (p-1) * (q-1)))
                
                rp = d % 2 != 0
            except ValueError:
                pass
        
        n = p*q

        print e, n
        print d, n

        # (e,n) public key
        # (d,n) secret key

        return RSAKey(RSAPublicKey(e,n), RSAPrivateKey(d,n))

    def sign(self, hash):
        out = []
        for c in hash:
            out.append(mod_exp(ord(c), self.priv_key.d, self.priv_key.n))
        
        return out
    
    def verify(self, hash, signature):
        out = []

        for c in signature:
            out.append(chr(mod_exp(c, self.public_key.e, self.public_key.n)))

        return "".join(out) == hash

if __name__ == '__main__':
    #print mod_exp(7, 560000000000000000000000000000000000, 561000000000000000000000000000000000)

    """
    print get_random_large_prime()
    print get_random_large_prime()
    print get_random_large_prime()
    
    print is_prime(3)
    print is_prime(4)
    print is_prime(3967)
    print is_prime(7691)
    print is_prime(7690)
  
    print mod_exp(7, 560, 561)
    """

    bug1 = 93128803
    bug2 = 272489629

    d = long(mul_inv(17, (bug1-1) * (bug2-1)))

    print "d", d

    key = RSAKey.generate_key()
    
    ver = key.verify("Jorma", key.sign("Jorma"))

    print ver
    
   
    


        

