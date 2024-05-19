#!/usr/bin/python3


from pysaber.rng import DRBG_ctx, randombytes, randombytes_init


def main():

    entropy_input = bytearray(48)

    for i in range(48):
        entropy_input[i] = i

    print(entropy_input.hex())

    randombytes_init(entropy_input)
    
    ##

    x = bytearray(32)

    randombytes(x, 32)

    pass

if __name__ == "__main__":
    main()
