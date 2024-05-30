import hashlib

import numpy as np

from pysaber.rng import randombytes
from pysaber.saber_indcpa import indcpa_kem_keypair
from pysaber.saber_params import (SABER_INDCPA_PUBLICKEYBYTES,
                                  SABER_INDCPA_SECRETKEYBYTES, SABER_KEYBYTES,
                                  SABER_SECRETKEYBYTES)


def crypto_kem_keypair(pk, sk):

    indcpa_kem_keypair(pk, sk)

    for i in range(SABER_INDCPA_PUBLICKEYBYTES):
        sk[i + SABER_INDCPA_SECRETKEYBYTES] = pk[i]

    hash_pk = hashlib.sha3_256(pk[:SABER_INDCPA_PUBLICKEYBYTES]).digest()

    sk[SABER_SECRETKEYBYTES - 64:SABER_SECRETKEYBYTES - 64 + SABER_KEYBYTES] = [np.uint8(x) for x in hash_pk]

    randombytes(sk[SABER_SECRETKEYBYTES - SABER_KEYBYTES:], SABER_KEYBYTES)


def crypto_kem_enc(c, k, pk):
    pass


def crypto_kem_dec(k, c, sk):
    pass
