import DS
from random import randrange

def gen_random_tx(q, p, g):
    serialNumber = randrange(0, (2**128) - 1)
    payerPrivateKey, payerPublicKey = DS.KeyGen(q, p, g)
    payeePrivateKey, payeePublicKey = DS.KeyGen(q, p, g)
    amount = randrange(1, 1000000)
    s, r = DS.SignGen(serialNumber, q, p, g, payerPrivateKey)

    tx = "*** Bitcoin transaction ***" + '\n'
    tx = tx + "Serial number:" + str(serialNumber) + '\n'
    tx = tx + "Payer public key (beta):" + str(payerPublicKey) + '\n'
    tx = tx + "Payee public key (beta):" + str(payeePublicKey) + '\n'
    tx = tx + "Amount:" + str(amount) + '\n'
    tx = tx + "Signature (s):" + str(s) + '\n'
    tx = tx + "Signature (r):" + str(r) + '\n'

    return tx