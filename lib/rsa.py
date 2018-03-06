"""
This RSA implementation is based on Introduction to Algorithms 3rd ed.
by Cormen, Leiserson, Rivest and Stein and is simply
for educational purposes.
"""
import sys
import math
from math import floor, log, sqrt
from random import randrange, getrandbits
from base64 import Base64


def egcd(a, b):
    """
    Recursive version of extended euclid's algorithm
    for finding greatest common divisor with coefficients
    x and y.
    """
    if b == 0:
        return (a, 1, 0)
    else:
        (d, x, y) = egcd(b, a % b)
        return (d, y, x - long(a/b) * y)


def mul_inv(a, b):
    """
    Calculate multiplicative inverse.
    """
    (d, x, _) = egcd(a, b)

    if d != 1:
        raise ValueError

    return x % b


def mod_exp(a, b, n):
    """
    Modular exponentation for big b's.
    """
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
    Miller-Rabin tests whether our random
    numbers are primes or not.
    """
    def witness(a, n):
        u = n - 1
        t = 0

        while u % 2 == 0:
            u >>= 1
            t += 1

        x = mod_exp(a, u, n)

        for _ in range(0, t):
            xp = x
            x = pow(x, 2, n)

            if x == 1 and xp != 1 and xp != n - 1:
                return True

        if x != 1:
            return True

        return False

    for _ in range(0, s):
        a = randrange(1, n-1)

        if witness(a, n):
            return False

    return True


def get_random_large_prime():
    """
    Returns insecure large random integer.
    """
    while 1:
        a = getrandbits(256)

        if a % 2 == 0:
            continue

        if is_prime(a):
            return a


class RSAUtils:
    @staticmethod
    def export_key(a, b):
        """
        Encode key to format base64(a:b)
        """
        return Base64().encode("{}:{}".format(a, b))

    @staticmethod
    def parse_key(data):
        """
        Decode key from format base64(a:b)
        """
        raw = Base64().decode(data)
        keys = raw.split(':')
        return (long(keys[0]), long(keys[1]))


class RSAPublicKey:
    def __init__(self, e, n):
        self.e = long(e)
        self.n = long(n)

    @staticmethod
    def load(data):
        e, n = RSAUtils.parse_key(data)
        return RSAPublicKey(e, n)

    def __str__(self):
        return RSAUtils.export_key(self.e, self.n)


class RSAPrivateKey:
    def __init__(self, d, n):
        self.d = long(d)
        self.n = long(n)

    @staticmethod
    def load(data):
        d, n = RSAUtils.parse_key(data)
        return RSAPrivateKey(d, n)

    def __str__(self):
        return RSAUtils.export_key(self.d, self.n)


class RSAKey:
    """
    RSA implementation based on CLRS.
    """
    def __init__(self, public_key, priv_key):
        """
        @type public_key: RSAPublicKey
        @type private_key: RSAPrivateKey
        """
        self.public_key = public_key
        self.priv_key = priv_key

    @staticmethod
    def generate_key(e=17):
        """
        Generate new key

        @param e: Small primary number used for public key. Default is 17.
        @return: RSAKey
        """
        rp = False

        # Loop until gcd(e, (p-1)*(q-1)) = 1
        while not rp:
            try:
                p = get_random_large_prime()
                q = get_random_large_prime()
                d = long(mul_inv(e, (p-1) * (q-1)))

                rp = True
            except ValueError:
                pass

        n = p*q

        # (e,n) public key
        # (d,n) secret key

        return RSAKey(RSAPublicKey(e, n), RSAPrivateKey(d, n))

    def sign(self, hash):
        """
        Sign hash with this key.

        @type hash: string
        """
        return map(lambda c: mod_exp(ord(c), self.priv_key.d, self.priv_key.n),
                   hash)

    def verify(self, hash, signature):
        """
        Verify hash with given signature.

        @type hash: string
        @type signature: int[]
        """
        out = []

        try:
            out = map(lambda c: chr(mod_exp(c,
                                            self.public_key.e,
                                            self.public_key.n)),
                      signature)
        except:
            """
            If this raises some random exception, key is definitely invalid.
            """
            return False

        return "".join(out) == hash

    def publickey(self):
        """
        Returns public key as a string. This means base64
        encoded presentation.
        """
        return str(self.public_key)

    def privatekey(self):
        """
        Returns private key as a string. This means base64
        encoded presentation.
        """
        return str(self.priv_key)

if __name__ == '__main__':
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
    """
    bug1 = 93128803
    bug2 = 272489629

    d = long(mul_inv(17, (bug1-1) * (bug2-1)))

    print "d", d

    key = RSAKey.generate_key()

    ver = key.verify("Jorma", key.sign("Jorma"))

    print ver"""

    def get_random_odd_number(bits):
        while True:
            r = getrandbits(bits)
            if r % 2 == 1:
                return r

    tries = []
    for i in range(1000):
        j = 0

        while not is_prime(getrandbits(256), s=40):
            j += 1

        tries.append(j)

    """print ("Avg Tries: ", (sum(tries) / float(len(tries))))"""
