import math 
import hashlib

def Hash(s):
    return hashlib.sha3_256(s).digest() 

def CheckPow(p, q, g, PoWLen, TxCnt, filename):
    file = open(filename, "r")
    lines = file.readlines()
    allTx = [None] * TxCnt
    index = 0
    file.close()
    
    for curLine in range(0, len(lines) - 1, 7):
        allTx[index] = lines[curLine] + lines[curLine + 1] + lines[curLine + 2] + lines[curLine + 3] + lines[curLine + 4] + lines[curLine + 5] + lines[curLine + 6]
        index += 1
    
    previousDepth = []

    for i in range(0, len(allTx)):
        previousDepth.append(Hash(allTx[i].encode("UTF-8")))

    while len(previousDepth) != 1:
        currentDepth = []
        for j in range(0, len(previousDepth), 2):
            concatStr = previousDepth[j] + previousDepth[j + 1]
            hashedStr = Hash(concatStr)
            currentDepth.append(hashedStr)
        previousDepth = currentDepth

    file = open(filename, 'r')
    lines = file.read().splitlines()
    file.close()
    nonce = lines[-1][7:]
    
    rootHash = previousDepth[0]

    print(rootHash)

    concatenated = rootHash + str(nonce).encode("UTF-8") + b"\n"
    proofOfWorkStr = hashlib.sha3_256(concatenated).hexdigest()

    return str(proofOfWorkStr)