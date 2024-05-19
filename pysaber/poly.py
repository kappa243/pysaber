
import hashlib

from pysaber.pack_unpack import BS2POLVECq
from pysaber.saber_params import SABER_L, SABER_POLYVECBYTES


def gen_matrix(A, seed):
    buf = hashlib.shake_128(seed).digest(SABER_L * SABER_POLYVECBYTES)

    for i in range(SABER_L):
        BS2POLVECq(buf[i * SABER_POLYVECBYTES:], A[i])