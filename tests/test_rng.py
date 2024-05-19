import pytest


def test_randombytes_init():
    from pysaber.rng import DRBG_ctx, randombytes_init

    entropy_input = bytearray(48)

    for i in range(48):
        entropy_input[i] = i

    randombytes_init(entropy_input)

    assert DRBG_ctx.Key.hex() == "530e88f8c34030bea16abefac8c67d84deb6522e59757d791f57dfc8a6ee8307"
    assert DRBG_ctx.V.hex() == "524121e913830c53f98bdfa5592b1ba1"


def test_randombytes():
    from pysaber.rng import randombytes, randombytes_init

    entropy_input = bytearray(48)

    for i in range(48):
        entropy_input[i] = i

    randombytes_init(entropy_input)

    x = bytearray(32)

    # 1 iter
    randombytes(x, 32)
    assert x.hex() == "061550234d158c5ec95595fe04ef7a25767f2e24cc2bc479d09d86dc9abcfde7"

    # 2 iter
    randombytes(x, 32)

    assert x.hex() == "1a9fbcbc8da36dff2abe203296170fdb97c3297f67fcb679ac719c9fd00253b0"

    # 3 iter
    randombytes(x, 32)

    assert x.hex() == "b2f004f5435f10c4cd451148447afd9b99b209770de0d03acdb7bc6be571688c"
