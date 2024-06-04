import hashlib

import numpy as np

from pysaber.rng import randombytes
from pysaber.saber_indcpa import indcpa_kem_keypair, indcpa_kem_enc
from pysaber.saber_params import (SABER_INDCPA_PUBLICKEYBYTES,
                                  SABER_INDCPA_SECRETKEYBYTES, SABER_KEYBYTES,
                                  SABER_SECRETKEYBYTES, SABER_BYTES_CCA_DEC)

def crypto_kem_keypair(pk, sk):

    indcpa_kem_keypair(pk, sk)

    for i in range(SABER_INDCPA_PUBLICKEYBYTES):
        sk[i + SABER_INDCPA_SECRETKEYBYTES] = pk[i]

    hash_pk = hashlib.sha3_256(pk[:SABER_INDCPA_PUBLICKEYBYTES]).digest()

    sk[SABER_SECRETKEYBYTES - 64:SABER_SECRETKEYBYTES - 64 + SABER_KEYBYTES] = [np.uint8(x) for x in hash_pk]

    randombytes(sk[SABER_SECRETKEYBYTES - SABER_KEYBYTES:], SABER_KEYBYTES)


def crypto_kem_enc(c, k, pk):
    # key encapsulation mechanism
    kr = np.zeros(64, dtype=np.uint8)
    buf = np.zeros(64, dtype=np.uint8)
    
    randombytes(buf, 32)
    buf[:32] = np.frombuffer(hashlib.sha3_256(buf[:32]).digest(), dtype=np.uint8)
    buf[32:] = np.frombuffer(hashlib.sha3_256(pk[:SABER_INDCPA_PUBLICKEYBYTES]).digest(), dtype=np.uint8)

    kr = np.frombuffer(hashlib.sha3_512(buf).digest(), dtype=np.uint8).copy()

    indcpa_kem_enc(buf[:32], kr[32:], pk, c)

    kr[32:] = np.frombuffer(hashlib.sha3_256(c[:SABER_BYTES_CCA_DEC]).digest(), dtype=np.uint8)

    k[:] = np.frombuffer(hashlib.sha3_256(kr).digest(), dtype=np.uint8)



def crypto_kem_dec(k, c, sk):
    pass
