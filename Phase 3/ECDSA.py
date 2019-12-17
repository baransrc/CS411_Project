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
    # print("KeyGen")

    order = E.order

    generator = E.generator

    privateKey = random.randint(2, order - 1)

    publicKey = generator * privateKey

    # print("Private Key: %d \nPublic Key X: %d \nPublic Key Y: %d" % (privateKey, publicKey.x, publicKey.y))

    return privateKey, publicKey


def SignGen(message, E, sA):
    # print("SignGen")

    order = E.order

    generator = E.generator

    hashedMessage = int(SHA3_256.new(message).hexdigest(), 16)

    r = 0
    s = 0

    while r == 0 or s == 0:
        k = random.randint(2, order - 1)

        randomPoint = k * generator

        r = randomPoint.x

        k_inv = modinv(k, order)

        s = (k_inv * (hashedMessage + (r * sA))) % order

    return s, r

def SignVer(message, s, r, E, QA):
    # print("SignVer")

    order = E.order

    generator = E.generator

    hashedMessage = int(SHA3_256.new(message).hexdigest(), 16)

    print(hashedMessage)

    s_inv = modinv(s, order)

    u1 = (hashedMessage * s_inv) % order
    u2 = (r * s_inv) % order

    randomPoint = (u1 * generator) + (u2 * QA) 

    # print("Random Point X: %d \nRandom Point Y: %d" % (randomPoint.x, randomPoint.y))

    acquired_r = randomPoint.x % order

    print(acquired_r)
    print(r)

    return 0 if (acquired_r == r) else 1