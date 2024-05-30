import hashlib

import numpy as np

from pysaber.cbd import cbd
from pysaber.pack_unpack import BS2POLVECq
from pysaber.poly_mul import poly_mul_acc
from pysaber.saber_params import (SABER_L, SABER_N, SABER_POLYCOINBYTES,
                                  SABER_POLYVECBYTES)


def gen_matrix(A, seed):
    buf = hashlib.shake_128(seed).digest(SABER_L * SABER_POLYVECBYTES)

    for i in range(SABER_L):
        BS2POLVECq(buf[i * SABER_POLYVECBYTES :], A[i])


def gen_secret(s, seed):
    buf = hashlib.shake_128(seed).digest(SABER_L * SABER_POLYCOINBYTES)

    for i in range(SABER_L):
        buf_view = memoryview(buf)[i * SABER_POLYCOINBYTES :]
        cbd(s[i], buf_view)


def matrix_mul(A, s, res, transpose):
    for i in range(SABER_L):
        for j in range(SABER_L):
            if transpose == 1:
                poly_mul_acc(A[j][i], s[j], res[i])
            else:
                poly_mul_acc(A[i][j], s[j], res[i])
