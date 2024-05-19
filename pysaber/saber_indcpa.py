import hashlib

import numpy as np

from pysaber.poly import gen_matrix
from pysaber.rng import randombytes
from pysaber.saber_params import (SABER_EP, SABER_EQ, SABER_ET, SABER_L,
                                  SABER_N, SABER_SEEDBYTES)

H1 = 1 << (SABER_EQ - SABER_EP - 1)
H2 = (1 << (SABER_EP - 2)) - (1 << (SABER_EP - SABER_ET - 1)) + (1 << (SABER_EQ - SABER_EP - 1))


def indcpa_kem_keypair(pk, sk):
    A = np.zeros((SABER_L, SABER_L, SABER_N), dtype=np.int16)
    s = np.zeros((SABER_L, SABER_N), dtype=np.int16)
    b = np.zeros((SABER_L, SABER_N), dtype=np.int16)

    seed_A = bytearray(SABER_SEEDBYTES)
    seed_s = bytearray(SABER_SEEDBYTES)

    randombytes(seed_A, SABER_SEEDBYTES)
    seed_A = hashlib.shake_128(seed_A).digest(SABER_SEEDBYTES)
    randombytes(seed_s, SABER_SEEDBYTES)

    gen_matrix(A, seed_A)

    pass


def indcpa_kem_enc(m, seed_sp, pk, ciphertext):
    pass


def indcpa_kem_dec(sk, ciphertext, m):
    pass
