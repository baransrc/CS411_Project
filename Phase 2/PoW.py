import math 
from Crypto.Hash import SHA3_256

def compHash(strTohash):
    shaObj = SHA3_256.new() 
    data = strTohash.encode('utf-8')
    h = int((shaObj.update(data)).hexdigest(), 16)
    del shaObj
    return h

def CheckPow(p, q, g, PoWLen, TxCnt, filename):
    file = open(filename, "r")
    lines = file.readlines()
    allSigns = [None] * TxCnt
    index = 0
    file.close()
    
    for curLine in range(5, len(lines), 7):
        allSigns[index] = lines[curLine][15:]
        index += 1
        
    hashTree = []
    temp = []
    for sign in allSigns:
        h = compHash(sign)
        temp.append(h)
    
    hashTree.append(temp)
    depth = int(math.log(TxCnt,2))

    for i in range(0, depth):
        temp = []
        for j in range(0, len(hashTree[i]), 2):
            tempStr = str(hashTree[i][j]) + str(hashTree[i][j + 1])
            h = compHash(tempStr)
            temp.append(h)
        hashTree.append(temp)
    
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        nonce = lines[-1][7:-1]
    
    
    rootHash = hashTree[len(hashTree) - 1][0]
    strReturn = str(rootHash) + nonce
    
    h = compHash(strReturn)
    
    strReturn = str(h)
    print(strReturn)
    
    return strReturn
        