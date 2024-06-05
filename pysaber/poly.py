# For further context refer to section 8.3.8 of documentation

import hashlib

import numpy as np

from pysaber.cbd import cbd
from pysaber.pack_unpack import BS2POLVECq
from pysaber.poly_mul import poly_mul_acc
from pysaber.saber_params import (SABER_L, SABER_N, SABER_POLYCOINBYTES,
                                  SABER_POLYVECBYTES)


def gen_matrix(A, seed):
    """
    Generate a matrix A using a given seed. The matrix A is populated with polynomial vectors.

    Parameters:
    A (list): The matrix to be generated, which is a list of polynomial vectors.
    seed (bytes): The seed used for generating the matrix.

    The method uses the SHAKE-128 hash function to generate a digest based on the seed. 
    This digest is then divided into chunks, each of which is converted into a polynomial vector 
    and stored in the corresponding position of the matrix A.
    """
    buf = hashlib.shake_128(seed).digest(SABER_L * SABER_POLYVECBYTES)

    for i in range(SABER_L):
        BS2POLVECq(buf[i * SABER_POLYVECBYTES :], A[i])


def gen_secret(s, seed):
    """
    Generate a secret vector s using a given seed. The secret vector is populated with polynomials.

    Parameters:
    s (list): The secret vector to be generated, which is a list of polynomials.
    seed (bytes): The seed used for generating the secret vector.

    The method uses the SHAKE-128 hash function to generate a digest based on the seed. 
    This digest is then divided into chunks, each of which is used to generate a polynomial 
    through a central binomial distribution (CBD) function and stored in the corresponding 
    position of the secret vector s.
    """
    buf = hashlib.shake_128(seed).digest(SABER_L * SABER_POLYCOINBYTES)

    for i in range(SABER_L):
        buf_view = memoryview(buf)[i * SABER_POLYCOINBYTES :]
        cbd(s[i], buf_view)


def matrix_mul(A, s, res, transpose):
    """
    Perform matrix-vector multiplication and store the result in `res`.
    
    Args:
        A (np.ndarray): Input matrix.
        s (np.ndarray): Input vector.
        res (np.ndarray): Result vector to store the product.
        transpose (int): If 1, transpose the matrix A before multiplication.
        q (int): Coefficient modulus.
    """
    for i in range(SABER_L):
        for j in range(SABER_L):
            if transpose == 1:
                poly_mul_acc(A[j][i], s[j], res[i])
            else:
                poly_mul_acc(A[i][j], s[j], res[i])


# For further context on method inner_prod reffer to section 8.3.9 in documentation
def inner_prod(b, s, res):
  """
  This function computes the inner product of two matrices b and s,
  and stores the result in the vector res.

  Args:
      b: A list of lists representing a matrix of size SABER_L x SABER_N.
      s: A list of lists representing a matrix of size SABER_L x SABER_N.
      res: A list to store the inner product result.

  Returns:
      None
  """
  for j in range(SABER_L):
    poly_mul_acc(b[j], s[j], res)


def shift_left(pin, shift):
    pout = np.zeros(SABER_N, dtype=np.uint16)
    for i in range(SABER_N - 1):
        pout[i] = (pin[i] << shift) | (pin[i + 1] >> (8 - shift))
    pout[SABER_N - 1] = pin[SABER_N - 1] << shift
    return pout


def shift_right(pin, shift):
    pout = np.zeros(SABER_N, dtype=np.uint16)
    for i in range(SABER_N - 1, 0, -1):
        pout[i] = (pin[i] >> shift) | (pin[i - 1] << (8 - shift))
    pout[0] = pin[0] >> shift
    return pout