
def rng_init():
    from pysaber.rng import randombytes_init

    entropy_input = bytearray(48)

    for i in range(48):
        entropy_input[i] = i

    randombytes_init(entropy_input)
