#!/usr/bin/python3


import hashlib

from pysaber.rng import randombytes_init
from pysaber.saber_indcpa import indcpa_kem_keypair
from pysaber.saber_params import SABER_NOISE_SEEDBYTES, SABER_SEEDBYTES


def main():

    entropy_input = bytearray(48)

    for i in range(48):
        entropy_input[i] = i

    randombytes_init(entropy_input)
    
    ##
    
    indcpa_kem_keypair(None, None)
        

    pass

if __name__ == "__main__":
    main()
