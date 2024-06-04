import hashlib

import numpy as np

from pysaber.pack_unpack import POLVECp2BS, POLVECq2BS, BS2POLVECp, BS2POLmsg, POLT2BS
from pysaber.poly import gen_matrix, gen_secret, matrix_mul, inner_prod, shift_left, shift_right
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
    """
    Generate a public and secret key pair using the SABER KEM IND-CPA secure key generation scheme.

    Parameters:
    pk (bytearray): The public key byte string, which will include the packed b and seed_A.
    sk (bytearray): The secret key byte string, which will include the packed secret vector s.

    Returns:
    tuple: A tuple containing the public key (pk) and the secret key (sk).
    """
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

    return pk, sk


def indcpa_kem_enc(m, seed_sp, pubkey, ciphertext):
    """
    Perform IND-CPA secure encryption using the SABER KEM encryption scheme.

    Parameters:
    m (bytes): The message bit string of length 256 to be encrypted.
    seed_sp (bytes): The random byte string of length SABER_SEEDBYTES used to generate the secret vector.
    pubkey (bytes): The public key used for encryption, which includes seedA and pk.
    ciphertext (bytearray): The resulting ciphertext byte string.

    Returns:
    bytearray: The ciphertext byte string.
    """
    pk, seedA = pubkey[:SABER_POLYVECCOMPRESSEDBYTES], pubkey[SABER_POLYVECCOMPRESSEDBYTES:]

    A = np.zeros((SABER_L, SABER_L, SABER_N), dtype=np.uint16)
    sp = np.zeros((SABER_L, SABER_N), dtype=np.uint16)
    bp = np.zeros((SABER_L, SABER_N), dtype=np.uint16)
    vp = np.zeros((SABER_N), dtype=np.uint16)
    b = np.zeros((SABER_L, SABER_N), dtype=np.uint16)
    mp = np.zeros((SABER_N), dtype=np.uint16)

    gen_matrix(A, seedA)
    gen_secret(sp, seed_sp)

    matrix_mul(A, sp, bp, 0)

    for i in range(SABER_L):
        for j in range(SABER_N):
            bp[i][j] = (bp[i][j] + H1) >> (SABER_EQ - SABER_EP)

    POLVECp2BS(ciphertext, bp)
    BS2POLVECp(pk, b)
    inner_prod(b, sp, vp)
    BS2POLmsg(m, mp)

    for i in range(SABER_N):
        vp[i] = (vp[i] - (mp[i] << (SABER_EP - 1)) + H1) >> (SABER_EP - SABER_ET)

    POLT2BS(ciphertext[SABER_POLYVECCOMPRESSEDBYTES:], vp)
    return ciphertext


def indcpa_kem_dec(sk, ciphertext, m):
    pass
