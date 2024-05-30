import hashlib

import numpy as np

from pysaber.pack_unpack import POLVECp2BS, POLVECq2BS
from pysaber.poly import gen_matrix, gen_secret, matrix_mul
from pysaber.rng import randombytes
from pysaber.saber_params import (SABER_EP, SABER_EQ, SABER_ET,
                                  SABER_INDCPA_PUBLICKEYBYTES,
                                  SABER_INDCPA_SECRETKEYBYTES, SABER_L,
                                  SABER_N, SABER_NOISE_SEEDBYTES,
                                  SABER_POLYVECCOMPRESSEDBYTES,
                                  SABER_SEEDBYTES)

H1 = 1 << (SABER_EQ - SABER_EP - 1)
H2 = (1 << (SABER_EP - 2)) - (1 << (SABER_EP - SABER_ET - 1)) + (1 << (SABER_EQ - SABER_EP - 1))


def indcpa_kem_keypair(pk, sk):
    A = np.zeros((SABER_L, SABER_L, SABER_N), dtype=np.uint16)
    s = np.zeros((SABER_L, SABER_N), dtype=np.uint16)
    b = np.zeros((SABER_L, SABER_N), dtype=np.uint16)

    seed_A = bytearray(SABER_SEEDBYTES)
    seed_s = bytearray(SABER_NOISE_SEEDBYTES)

    randombytes(seed_A, SABER_SEEDBYTES)
    seed_A = hashlib.shake_128(seed_A).digest(SABER_SEEDBYTES)
    randombytes(seed_s, SABER_NOISE_SEEDBYTES)

    gen_matrix(A, seed_A)
    gen_secret(s, seed_s)

    matrix_mul(A, s, b, 1)

    for i in range(SABER_L):
        for j in range(SABER_N):
            b[i][j] = (b[i][j] + H1) >> (SABER_EQ - SABER_EP)

    POLVECq2BS(sk, s)
    POLVECp2BS(pk, b)

    pk[SABER_POLYVECCOMPRESSEDBYTES:] = [np.uint8(x) for x in seed_A]

    pass


def indcpa_kem_enc(m, seed_sp, pk, ciphertext):
    pass


def indcpa_kem_dec(sk, ciphertext, m):
    pass
