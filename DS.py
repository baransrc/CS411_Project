import os
import os.path
from os import path
import pathlib
import sys
import time
import random
import string
from Crypto.Util import number

def Setup(candidate_p_count = 1, verbose = False):
    bitSizeP = 2048
    bitSizeQ = 224

    isPFound = False

    # Generate q and p:
    while isPFound == False:
        q = number.getPrime(bitSizeQ, os.urandom)
        p = 0

        maxP = (2**bitSizeP) - 1
        k = (maxP - 1) // q

        candidates = []

        while k > 1:
            k = k - 1
            p = (k*q) + 1

            if number.isPrime(p):
                isPFound = True
                candidates.append(p)
            
            if len(candidates) >= candidate_p_count:
                break
        
        p = random.choice(candidates)

    # Generate g:
    g = 1
    exponent = (p - 1) // q

    while g == 1:
        alpha = random.randint(1, p - 1)
        g = pow(alpha, exponent, p)

    if verbose:
        print("q: %d \n\np: %d \n\ng: %d" %(q, p, g))

    return q, p, g

def KeyGen(q, p, g):
    alpha = random.randint(0, q - 1)
    beta = pow(g, alpha, p)
    return alpha, beta

def GenerateOrRead(fileName, verbose = False):
    file = open(fileName, "a+")
    file.close()

    if os.stat(fileName).st_size == 0:
        q, p, g = Setup(verbose=True)
        fileStr = str(q) + '\n' + str(p) + '\n' + str(g)

        file = open(fileName, "w")
        file.write(fileStr)
        file.close()

    file = open(fileName, "r")
    q = int(file.readline())
    p = int(file.readline())
    g = int(file.readline())

    if verbose:
        print("q: %d \n\np: %d \n\ng: %d" %(q, p, g))

    return q, p, g

def random_string(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))