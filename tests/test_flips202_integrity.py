import hashlib

from pysaber.rng import randombytes
from pysaber.saber_params import SABER_SEEDBYTES
from tests.common import rng_init


def test_shake128():

    rng_init()

    seed_A = bytearray(SABER_SEEDBYTES)

    randombytes(seed_A, SABER_SEEDBYTES)
    assert seed_A.hex() == "061550234d158c5ec95595fe04ef7a25767f2e24cc2bc479d09d86dc9abcfde7"

    seed_A = hashlib.shake_128(seed_A).digest(SABER_SEEDBYTES)
    assert seed_A.hex() == "078800a7a766be5e244ad3fce29e39839cfe82c9aaabf27ccf2fc653562d938f"
