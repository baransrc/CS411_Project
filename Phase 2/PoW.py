import math 
from Crypto.Hash import SHA3_256

def compHash(strTohash):
    shaObj = SHA3_256.new() 
    data = strTohash.encode('utf-8')
    h = (shaObj.update(data)).hexdigest()
    del shaObj
    return h

def CheckPow(p, q, g, PoWLen, TxCnt, filename):
    file = open(filename, "r")
    lines = file.readlines()
    allSigns = [None] * TxCnt
    index = 0
    file.close()
    
    for curLine in range(0, len(lines) - 1, 7):
        allSigns[index] = lines[curLine + 2][25:].replace('\n', '') 
        + lines[curLine + 3][25:].replace('\n', '') 
        + lines[curLine + 5][15:].replace('\n', '') 
        + lines[curLine + 6][15:].replace('\n', '')
        print(allSigns[index])
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
        nonce = lines[-1][7:]

    
    rootHash = hashTree[len(hashTree) - 1][0]
    strReturn = str(rootHash) + nonce
    print("nonce is: ", nonce)
    h = compHash(strReturn)
    
    strReturn = str(h)
    print(strReturn)
    
    return strReturn
        