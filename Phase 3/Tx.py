import DS
from random import randrange
import math

def gen_random_tx(q, p, g):
    serialNumber = randrange(0, (2**128) - 1)
    payerPrivateKey, payerPublicKey = DS.KeyGen(q, p, g)
    payeePrivateKey, payeePublicKey = DS.KeyGen(q, p, g)
    amount = randrange(1, 1000000)
    s, r = DS.SignGen(serialNumber, q, p, g, payerPrivateKey)

    tx = "*** Bitcoin transaction ***" + '\n'
    tx = tx + "Serial number: " + str(serialNumber) + '\n'
    tx = tx + "Payer public key (beta): " + str(payerPublicKey) + '\n'
    tx = tx + "Payee public key (beta): " + str(payeePublicKey) + '\n'
    tx = tx + "Amount: " + str(amount) + '\n'
    tx = tx + "Signature (s): " + str(s) + '\n'
    tx = tx + "Signature (r): " + str(r) + '\n'

    return tx


def gen_random_txblock(q, p, g, txCount, filename):
    powTxCount = math.log2(txCount)

    if powTxCount.is_integer() == False:
        txCount = 2 ** math.floor(powTxCount) # if txCount is not a power of two, 
                                              # take highest power of two smaller than txCount

    transactionString = ""
    for i in range(0, txCount):
        transactionString += gen_random_tx(q, p, g)

    file = open(filename, 'w+')
    file.write(transactionString)
    file.close()
