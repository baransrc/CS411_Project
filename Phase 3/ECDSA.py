import random
import sys
from ecpy.curves import Curve
from Crypto.Hash import SHA3_256

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


def KeyGen(E):
    order = E.order

    generator = E.generator

    privateKey = random.randint(2, order - 1)

    publicKey = generator * privateKey

    # print("Private Key: %d \nPublic Key X: %d \nPublic Key Y: %d" % (privateKey, publicKey.x, publicKey.y))

    return privateKey, publicKey


def SignGen(message, E, sA):
    n = E.order

    G = E.generator

    h = int(SHA3_256.new(message).hexdigest(), 16)

    r = 0
    s = 0

    while r == 0 or s == 0:
        k = random.randint(1, n - 1)

        R = k * G

        r = R.x % n

        k_inv = modinv(k, n)

        s = (k_inv * (h + (sA * r))) % n

    return s, r

def SignVer(message, s, r, E, QA):
    n = E.order

    G = E.generator

    h = int(SHA3_256.new(message).hexdigest(), 16) 
    # I also tried: h = int.from_bytes(SHA3_256.new(message).digest(), "big")
    # And           h = int.from_bytes(SHA3_256.new(message).digest(), "little")

    s_inv = modinv(s, n)

    u1 = (h * s_inv) % n
    u2 = (r * s_inv) % n

    R = (u1 * G) + (u2 * QA) 

    # print("R X: %d \nR Y: %d" % (R.x, R.y))

    v = R.x % n

    r = r % n

    print("r: %d \nv: %d" % (r, v))

    return 0 if (v == r) else 1