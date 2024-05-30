import numpy as np

from pysaber.saber_params import SABER_MU, SABER_N


def cbd(s, buf):
    if SABER_MU == 6:
        for i in range(SABER_N // 4):
            buf_view = memoryview(buf)[3 * i:3 * i + 3]
            t = int.from_bytes(buf_view, 'little')
            d = 0
            for j in range(3):
                d += (t >> j) & 0x249249

            a = [0] * 4
            b = [0] * 4
            a[0] = d & 0x7
            b[0] = (d >> 3) & 0x7
            a[1] = (d >> 6) & 0x7
            b[1] = (d >> 9) & 0x7
            a[2] = (d >> 12) & 0x7
            b[2] = (d >> 15) & 0x7
            a[3] = (d >> 18) & 0x7
            b[3] = (d >> 21)

            s[4 * i + 0] = np.array(a[0] - b[0]).astype(np.uint16)
            s[4 * i + 1] = np.array(a[1] - b[1]).astype(np.uint16)
            s[4 * i + 2] = np.array(a[2] - b[2]).astype(np.uint16)
            s[4 * i + 3] = np.array(a[3] - b[3]).astype(np.uint16)

    elif SABER_MU == 8:
        for i in range(SABER_N // 4):
            buf_view = memoryview(buf)[4 * i:4 * i + 4]
            t = int.from_bytes(buf_view, 'little')
            d = 0
            for j in range(4):
                d += (t >> j) & 0x11111111

            a = [0] * 4
            b = [0] * 4
            a[0] = d & 0xf
            b[0] = (d >> 4) & 0xf
            a[1] = (d >> 8) & 0xf
            b[1] = (d >> 12) & 0xf
            a[2] = (d >> 16) & 0xf
            b[2] = (d >> 20) & 0xf
            a[3] = (d >> 24) & 0xf
            b[3] = (d >> 28)

            s[4 * i + 0] = np.array(a[0] - b[0]).astype(np.uint16)
            s[4 * i + 1] = np.array(a[1] - b[1]).astype(np.uint16)
            s[4 * i + 2] = np.array(a[2] - b[2]).astype(np.uint16)
            s[4 * i + 3] = np.array(a[3] - b[3]).astype(np.uint16)

    elif SABER_MU == 10:
        for i in range(SABER_N // 4):
            buf_view = memoryview(buf)[5 * i:5 * i + 5]
            t = int.from_bytes(buf_view, 'little')
            d = 0
            for j in range(5):
                d += (t >> j) & 0x0842108421

            a = [0] * 4
            b = [0] * 4
            a[0] = d & 0x1f
            b[0] = (d >> 5) & 0x1f
            a[1] = (d >> 10) & 0x1f
            b[1] = (d >> 15) & 0x1f
            a[2] = (d >> 20) & 0x1f
            b[2] = (d >> 25) & 0x1f
            a[3] = (d >> 30) & 0x1f
            b[3] = (d >> 35)

            s[4 * i + 0] = np.array(a[0] - b[0]).astype(np.uint16)
            s[4 * i + 1] = np.array(a[1] - b[1]).astype(np.uint16)
            s[4 * i + 2] = np.array(a[2] - b[2]).astype(np.uint16)
            s[4 * i + 3] = np.array(a[3] - b[3]).astype(np.uint16)
    else:
        raise ValueError("Unsupported SABER parameter.")