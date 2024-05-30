#!/usr/bin/python3



import numpy as np

from pysaber.api import CRYPTO_PUBLICKEYBYTES, CRYPTO_SECRETKEYBYTES
from pysaber.kem import crypto_kem_keypair
from pysaber.rng import randombytes_init
from pysaber.saber_indcpa import indcpa_kem_keypair

np.seterr(over="ignore")


def main():

    pk = np.zeros(CRYPTO_PUBLICKEYBYTES, dtype=np.uint8)
    sk = np.zeros(CRYPTO_SECRETKEYBYTES, dtype=np.uint8)

    entropy_input = bytearray(48)

    for i in range(48):
        entropy_input[i] = i

    randombytes_init(entropy_input)

    ##

    # indcpa_kem_keypair(pk, sk)
    crypto_kem_keypair(pk, sk)

    pass


if __name__ == "__main__":
    main()
