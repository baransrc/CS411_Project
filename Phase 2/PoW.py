import math 
import hashlib

def listToString(s):  
    str1 = ""  
    for elm in s:  
        str1 += elm
    return str1  

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
            concat = previousDepth[j] + previousDepth[j + 1]
            hashedStr = Hash(concat)
            currentDepth.append(hashedStr)
        previousDepth = currentDepth

    file = open(filename, 'r')
    lines = file.read().splitlines()
    file.close()
    nonce = lines[-1][7:]
    
    rootHash = previousDepth[0]

    print(rootHash)

    concatenated = rootHash + str(nonce + "\n").encode("UTF-8")
    proofOfWorkStr = hashlib.sha3_256(concatenated).hexdigest()

    return str(proofOfWorkStr)

def PoW(PoWLen, q, p, g, TxCnt, filename):
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
            concat = previousDepth[j] + previousDepth[j + 1]
            hashedStr = Hash(concat)
            currentDepth.append(hashedStr)
        previousDepth = currentDepth

    
    rootHash = previousDepth[0]

    print(rootHash)

    for nonce in range(0, 2**32):
        str(nonce)
        concatenated = rootHash + (str(nonce) + "\n").encode("UTF-8")
        proofOfWorkStr = hashlib.sha3_256(concatenated).hexdigest()
        if(proofOfWorkStr[:PoWLen] == PoWLen * "0"):
            break
            
    lines.append("Nonce: " + str(nonce))
    return listToString(lines)

def PowCompetitive(PoWLen, q, p, g, TxCnt, filename):
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
            concat = previousDepth[j] + previousDepth[j + 1]
            hashedStr = Hash(concat)
            currentDepth.append(hashedStr)
        previousDepth = currentDepth

    
    rootHash = previousDepth[0]

    print(rootHash)

    maxLen = PoWLen - 1
    for nonce in range(0, 2**32):
        strNonce = str(nonce)
        concatenated = rootHash + (strNonce + "\n").encode("UTF-8")
        proofOfWorkStr = hashlib.sha3_256(concatenated).hexdigest()
        
        length = 0
        while True:
            if (proofOfWorkStr[length] != '0'):
                break
            length += 1

        if (length > maxLen):
            maxLen = length
            print("Nonce: %d\nLength: %d\nPoW: %s\n" %(nonce, length, proofOfWorkStr))