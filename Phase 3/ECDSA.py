import random
import sys
from ecpy.curves import Curve, Point
from Crypto.Hash import SHA3_256
import secrets

def ModularInversePrime(k, p):
    return pow(k, p - 2, p)

def EllipticSum(Px, Py, Qx, Qy, E):
    a = E.a
    b = E.b
    p = E.field

    Lambda = 0

    Px = Px % p
    Py = Py % p
    Qx = Qx % p
    Qy = Qy % p

    if Px == Qx and Py == Qy:
        Lambda = (((3 * ((Px)**2)) + a) * ModularInversePrime(2 * Py, p)) % p
    else:
        Lambda = ((Py - Qy) * ModularInversePrime(Px - Qx, p)) % p

    x = ((Lambda**2) - Px - Qx) % p
    y = ((Lambda * (Px - x)) -Py) % p

    return x, y

def EllipticMultiplication(Px, Py, k, E):
    Tx = Px
    Ty = Py
    Qx = 0
    Qy = 0
    
    firstTime = True

    while k != 0:
        if (k % 2) != 0:
            if firstTime == True:
                Qx = Tx
                Qy = Ty
                firstTime = False
            else:
                Qx, Qy = EllipticSum(Qx, Qy, Tx, Ty, E)
        
        k = k // 2

        if k != 0:
            Tx, Ty = EllipticSum(Tx, Ty, Tx, Ty, E)
    
    return Qx, Qy        

def KeyGen(E):
    n = E.order
    P = E.generator

    sA = secrets.randbelow(n-1)
    x, y = EllipticMultiplication(P.x, P.y, sA, E)

    QA = Point(x, y, E)

    # print("Private Key: %d \nPublic Key X: %d \nPublic Key Y: %d" % (sA, QA.x, QA.y))

    return sA, QA

def Hash(msg):
    hashBytes = SHA3_256.new(msg).digest()
    return int.from_bytes(hashBytes, byteorder="big")

def SignGen(message, E, sA):
    n = E.order

    P = E.generator

    h = Hash(message) % n

    r = 0
    s = 0

    while r == 0 or s == 0:
        k = secrets.randbelow(n)

        Rx, Ry = EllipticMultiplication(P.x, P.y, k, E)

        r = (Rx) % n

        k_inv = ModularInversePrime(k, n)

        s = ((k_inv * (h + (sA * r))) % n)

    return s, r

def SignVer(message, s, r, E, QA): 
    n = E.order
    P = E.generator
    h = Hash(message) % n

    s_inv = ModularInversePrime(s, n)

    u1 = (h * s_inv) % n
    u2 = (r * s_inv) % n

    u1P_x, u1P_y = EllipticMultiplication(P.x, P.y, u1, E)
    u2QA_x, u2QA_y = EllipticMultiplication(QA.x, QA.y, u2, E)

    Rx, Ry = EllipticSum(u1P_x, u1P_y, u2QA_x, u2QA_y, E)

    v = (Rx) % n

    r = r % n

    print("v: %d \nr: %d" % (v, r))

    return 0 if (v == r) else 1