from Crypto.Hash import SHA3_256
import secrets

def AddBlock2Chain(PoWLen, TxCnt, block_candidate, PrevBlock):
    
    newBlock = block_candidate
    rootHash = GetRootHash(newBlock)
    PrevPow = '00000000000000000000'

    if PrevBlock != "":
        PrevPow = str(PrevBlock[len(PrevBlock) - 2])[14:-1]

    Pow, nonce = FindPoWAndNonce(rootHash, PrevPow.encode("UTF-8"), PoWLen)
   
    PoWStr = "Previous PoW: " + str(Pow) + "\n"
    nonceStr = "Nonce: " + str(nonce) + "\n"
    
    newBlock.append(PoWStr)
    newBlock.append(nonceStr)

    strNewBlock = ""
    for i in range(0, len(newBlock)):
        strNewBlock = strNewBlock + str(newBlock[i])

    return strNewBlock, Pow

def FindPoWAndNonce(rootHash, PrevPow, PoWLen):
    nonce = 0
    PoW = ""

    for currentNonce in range(2**64, 0, -1):
        concatenated = rootHash + PrevPow + currentNonce.to_bytes((currentNonce.bit_length()+7)//8, byteorder="big")
        proofOfWorkStr = HashHexDigest(concatenated)
        if (proofOfWorkStr[:PoWLen] == "0" * PoWLen):
            nonce = currentNonce
            PoW = proofOfWorkStr
            break
    
    return PoW, nonce

def GetRootHash(Block):
    TxLen = 9
    TxCnt = len(Block)
    hashTree = []
    for i in range(0,TxCnt):
        transaction = "".join(Block[i*TxLen:(i+1)*TxLen])
        hashTree.append(SHA3_256.new(transaction.encode('UTF-8')).digest())
    t = TxCnt
    j = 0
    while(t>1):
        for i in range(j,j+t,2):
            hashTree.append(SHA3_256.new(hashTree[i]+hashTree[i+1]).digest())
        j += t
        t = t>>1

    return hashTree[2*TxCnt-2]

def HashDigest(msg):
    return SHA3_256.new(msg).digest()

def HashHexDigest(msg):
    return SHA3_256.new(msg).hexdigest()

def HashInt(msg):
    return int(HashHexDigest(msg), 16)