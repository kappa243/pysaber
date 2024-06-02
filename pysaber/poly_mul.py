#For further context refer to section 8.3.7 of documentation

import numpy as np

from pysaber.saber_params import SABER_N

np.seterr(over="ignore")

SCHB_N = 16

N_RES = SABER_N << 1
N_SB = SABER_N >> 2
N_SB_RES = 2 * N_SB - 1

KARATSUBA_N = 64


def OVERFLOWING_MUL(X, Y):
    """
    Multiplies two 16-bit unsigned integers and returns the lower 16 bits of the result.
    
    Args:
        X (np.uint16): First operand.
        Y (np.uint16): Second operand.

    Returns:
        np.uint16: The result of the multiplication truncated to 16 bits.
    """
    return np.uint16((np.uint32(X) * np.uint32(Y)))


def karatsuba_simple(a_1, b_1, result_final):
    """
    Performs a simple Karatsuba multiplication on the input polynomials and stores the result.

    Args:
        a_1 (np.ndarray): First input polynomial.
        b_1 (np.ndarray): Second input polynomial.
        result_final (np.ndarray): Array to store the result of the multiplication.
    """
    d01 = np.zeros(KARATSUBA_N // 2 - 1, dtype=np.uint16)
    d0123 = np.zeros(KARATSUBA_N // 2 - 1, dtype=np.uint16)
    d23 = np.zeros(KARATSUBA_N // 2 - 1, dtype=np.uint16)
    result_d01 = np.zeros(KARATSUBA_N - 1, dtype=np.uint16)

    result_d01.fill(0)
    d01.fill(0)
    d0123.fill(0)
    d23.fill(0)
    result_final.fill(0)

    for i in range(KARATSUBA_N // 4):
        acc1 = a_1[i]
        acc2 = a_1[i + KARATSUBA_N // 4]
        acc3 = a_1[i + 2 * KARATSUBA_N // 4]
        acc4 = a_1[i + 3 * KARATSUBA_N // 4]
        for j in range(KARATSUBA_N // 4):

            acc5 = b_1[j]
            acc6 = b_1[j + KARATSUBA_N // 4]

            result_final[i + j + 0 * KARATSUBA_N // 4] += OVERFLOWING_MUL(acc1, acc5)
            result_final[i + j + 2 * KARATSUBA_N // 4] += OVERFLOWING_MUL(acc2, acc6)

            acc7 = acc5 + acc6
            acc8 = acc1 + acc2
            d01[i + j] += np.uint16(acc7 * np.uint64(acc8))
            # --------------------------------------------------------

            acc7 = b_1[j + 2 * KARATSUBA_N // 4]
            acc8 = b_1[j + 3 * KARATSUBA_N // 4]
            result_final[i + j + 4 * KARATSUBA_N // 4] += OVERFLOWING_MUL(acc7, acc3)

            result_final[i + j + 6 * KARATSUBA_N // 4] += OVERFLOWING_MUL(acc8, acc4)

            acc9 = acc3 + acc4
            acc10 = acc7 + acc8
            d23[i + j] += OVERFLOWING_MUL(acc9, acc10)
            # --------------------------------------------------------

            acc5 = acc5 + acc7
            acc7 = acc1 + acc3
            result_d01[i + j + 0 * KARATSUBA_N // 4] += OVERFLOWING_MUL(acc5, acc7)

            acc6 = acc6 + acc8
            acc8 = acc2 + acc4

            result_d01[i + j + 2 * KARATSUBA_N // 4] += OVERFLOWING_MUL(acc6, acc8)

            acc5 = acc5 + acc6
            acc7 = acc7 + acc8
            d0123[i + j] += OVERFLOWING_MUL(acc5, acc7)

    # 2nd last stage

    for i in range(KARATSUBA_N // 2 - 1):
        d0123[i] -= result_d01[i + 0 * KARATSUBA_N // 4] + result_d01[i + 2 * KARATSUBA_N // 4]
        d01[i] -= result_final[i + 0 * KARATSUBA_N // 4] + result_final[i + 2 * KARATSUBA_N // 4]
        d23[i] -= result_final[i + 4 * KARATSUBA_N // 4] + result_final[i + 6 * KARATSUBA_N // 4]

    for i in range(KARATSUBA_N // 2 - 1):
        result_d01[i + 1 * KARATSUBA_N // 4] += d0123[i]
        result_final[i + 1 * KARATSUBA_N // 4] += d01[i]
        result_final[i + 5 * KARATSUBA_N // 4] += d23[i]

    # Last stage

    for i in range(KARATSUBA_N - 1):
        result_d01[i] -= result_final[i] + result_final[i + KARATSUBA_N]

    for i in range(KARATSUBA_N - 1):
        result_final[i + 1 * KARATSUBA_N // 2] += result_d01[i]


def toom_cook_4way(a1, b1, result):
    """
    Performs Toom-Cook 4-way multiplication on the input polynomials and stores the result.

    Args:
        a1 (np.ndarray): First input polynomial.
        b1 (np.ndarray): Second input polynomial.
        result (np.ndarray): Array to store the result of the multiplication.
    """
    inv3 = np.uint32(43691)
    inv9 = np.uint32(36409)
    inv15 = np.uint32(61167)

    aw1 = np.zeros(N_SB, dtype=np.uint16)
    aw2 = np.zeros(N_SB, dtype=np.uint16)
    aw3 = np.zeros(N_SB, dtype=np.uint16)
    aw4 = np.zeros(N_SB, dtype=np.uint16)
    aw5 = np.zeros(N_SB, dtype=np.uint16)
    aw6 = np.zeros(N_SB, dtype=np.uint16)
    aw7 = np.zeros(N_SB, dtype=np.uint16)

    bw1 = np.zeros(N_SB, dtype=np.uint16)
    bw2 = np.zeros(N_SB, dtype=np.uint16)
    bw3 = np.zeros(N_SB, dtype=np.uint16)
    bw4 = np.zeros(N_SB, dtype=np.uint16)
    bw5 = np.zeros(N_SB, dtype=np.uint16)
    bw6 = np.zeros(N_SB, dtype=np.uint16)
    bw7 = np.zeros(N_SB, dtype=np.uint16)

    w1 = np.zeros(N_SB_RES, dtype=np.uint16)
    w2 = np.zeros(N_SB_RES, dtype=np.uint16)
    w3 = np.zeros(N_SB_RES, dtype=np.uint16)
    w4 = np.zeros(N_SB_RES, dtype=np.uint16)
    w5 = np.zeros(N_SB_RES, dtype=np.uint16)
    w6 = np.zeros(N_SB_RES, dtype=np.uint16)
    w7 = np.zeros(N_SB_RES, dtype=np.uint16)

    A0 = a1
    A1 = a1[N_SB:]
    A2 = a1[2 * N_SB :]
    A3 = a1[3 * N_SB :]
    B0 = b1
    B1 = b1[N_SB:]
    B2 = b1[2 * N_SB :]
    B3 = b1[3 * N_SB :]

    C = result

    for j in range(N_SB):
        r0 = A0[j]
        r1 = A1[j]
        r2 = A2[j]
        r3 = A3[j]
        r4 = r0 + r2
        r5 = r1 + r3
        r6 = r4 + r5
        r7 = r4 - r5
        aw3[j] = r6
        aw4[j] = r7
        r4 = np.uint16((np.uint16(r0 << 2) + r2) << 1)
        r5 = np.uint16(r1 << 2) + r3
        r6 = r4 + r5
        r7 = r4 - r5
        aw5[j] = r6
        aw6[j] = r7
        r4 = np.uint16(r3 << 3) + np.uint16(r2 << 2) + np.uint16(r1 << 1) + r0
        aw2[j] = r4
        aw7[j] = r0
        aw1[j] = r3

    for j in range(N_SB):
        r0 = B0[j]
        r1 = B1[j]
        r2 = B2[j]
        r3 = B3[j]
        r4 = r0 + r2
        r5 = r1 + r3
        r6 = r4 + r5
        r7 = r4 - r5
        bw3[j] = r6
        bw4[j] = r7
        r4 = np.uint16((np.uint16(r0 << 2) + r2) << 1)
        r5 = np.uint16(r1 << 2) + r3
        r6 = r4 + r5
        r7 = r4 - r5
        bw5[j] = r6
        bw6[j] = r7
        r4 = np.uint16(r3 << 3) + np.uint16(r2 << 2) + np.uint16(r1 << 1) + r0
        bw2[j] = r4
        bw7[j] = r0
        bw1[j] = r3

    karatsuba_simple(aw1, bw1, w1)
    karatsuba_simple(aw2, bw2, w2)
    karatsuba_simple(aw3, bw3, w3)
    karatsuba_simple(aw4, bw4, w4)
    karatsuba_simple(aw5, bw5, w5)
    karatsuba_simple(aw6, bw6, w6)
    karatsuba_simple(aw7, bw7, w7)

    for i in range(N_SB_RES):
        r0 = w1[i]
        r1 = w2[i]
        r2 = w3[i]
        r3 = w4[i]
        r4 = w5[i]
        r5 = w6[i]
        r6 = w7[i]

        r1 = r1 + r4
        r5 = r5 - r4
        r3 = np.uint16((np.uint32(r3) - r2) >> 1)
        r4 = r4 - r0
        r4 = r4 - np.uint16(r6 << 6)
        r4 = np.uint16(r4 << 1) + r5
        r2 = r2 + r3
        r1 = r1 - np.uint16(r2 << 6) - r2
        r2 = r2 - r6
        r2 = r2 - r0
        r1 = r1 + np.uint16(45) * r2
        r4 = (((r4 - (r2 << 3)) * inv3) >> 3).astype(np.uint16)
        r5 = r5 + r1
        r1 = (((r1 + (r3 << 4)) * inv9) >> 1).astype(np.uint16)
        r3 = -(r3 + r1)
        r5 = (((30 * r1 - r5) * inv15) >> 2).astype(np.uint16)
        r2 = r2 - r4
        r1 = r1 - r5

        r1 = np.uint16(r1)
        r2 = np.uint16(r2)
        r3 = np.uint16(r3)
        r4 = np.uint16(r4)
        r5 = np.uint16(r5)
        r6 = np.uint16(r6)

        C[i] += np.uint16(r6)
        C[i + 64] += np.uint16(r5)
        C[i + 128] += np.uint16(r4)
        C[i + 192] += np.uint16(r3)
        C[i + 256] += np.uint16(r2)
        C[i + 320] += np.uint16(r1)
        C[i + 384] += np.uint16(r0)


def poly_mul_acc(a, b, res):
    """
    Performs polynomial multiplication using the Toom-Cook 4-way algorithm and accumulates the result.

    Args:
        a (np.ndarray): First input polynomial.
        b (np.ndarray): Second input polynomial.
        res (np.ndarray): Array to accumulate the result of the multiplication.
    """
    c = np.zeros(2 * SABER_N, dtype=np.uint16)

    toom_cook_4way(a, b, c)

    for i in range(SABER_N, 2 * SABER_N):
        res[i - SABER_N] += c[i - SABER_N] - c[i]
