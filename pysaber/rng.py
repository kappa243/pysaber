from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Constants
RNG_SUCCESS = 0
RNG_BAD_MAXLEN = -1
RNG_BAD_OUTBUF = -2
RNG_BAD_REQ_LEN = -3


class AES_XOF_struct:
    def __init__(self):
        self.buffer = bytearray(16)
        self.buffer_pos = 16
        self.length_remaining = 0
        self.key = bytearray(32)
        self.ctr = bytearray(16)


class AES256_CTR_DRBG_struct:
    def __init__(self):
        self.Key = bytearray(32)
        self.V = bytearray(16)
        self.reseed_counter = 0


DRBG_ctx = AES256_CTR_DRBG_struct()


def AES256_ECB(key, ctr, buffer):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(ctr) + encryptor.finalize()
    buffer[: len(encrypted)] = encrypted


def seedexpander_init(ctx, seed, diversifier, maxlen):
    if maxlen >= 0x100000000:
        return RNG_BAD_MAXLEN

    ctx.length_remaining = maxlen
    ctx.key[:] = seed

    ctx.ctr[:8] = diversifier
    ctx.ctr[8:12] = [(maxlen >> (8 * i)) & 0xFF for i in range(4)][::-1]
    ctx.ctr[12:] = b"\x00\x00\x00\x00"

    ctx.buffer_pos = 16
    ctx.buffer[:] = b"\x00" * 16

    return RNG_SUCCESS


def seedexpander(ctx, x, xlen):
    if x is None:
        return RNG_BAD_OUTBUF
    if xlen >= ctx.length_remaining:
        return RNG_BAD_REQ_LEN

    ctx.length_remaining -= xlen
    offset = 0

    while xlen > 0:
        if xlen <= (16 - ctx.buffer_pos):
            x[offset : offset + xlen] = ctx.buffer[ctx.buffer_pos : ctx.buffer_pos + xlen]
            ctx.buffer_pos += xlen
            return RNG_SUCCESS

        x[offset : offset + (16 - ctx.buffer_pos)] = ctx.buffer[ctx.buffer_pos : 16]
        xlen -= 16 - ctx.buffer_pos
        offset += 16 - ctx.buffer_pos

        AES256_ECB(ctx.key, ctx.ctr, ctx.buffer)
        ctx.buffer_pos = 0

        for i in range(15, 11, -1):
            if ctx.ctr[i] == 0xFF:
                ctx.ctr[i] = 0x00
            else:
                ctx.ctr[i] += 1
                break

    return RNG_SUCCESS


def randombytes_init(entropy_input, personalization_string=None, security_strength=256):
    seed_material = bytearray(entropy_input[:48])
    if personalization_string:
        seed_material = bytearray([seed_material[i] ^ personalization_string[i] for i in range(48)])

    DRBG_ctx.Key[:] = b"\x00" * 32
    DRBG_ctx.V[:] = b"\x00" * 16
    AES256_CTR_DRBG_Update(seed_material, DRBG_ctx.Key, DRBG_ctx.V)
    DRBG_ctx.reseed_counter = 1


def randombytes(x, xlen):
    block = bytearray(16)
    i = 0

    while xlen > 0:
        for j in range(15, -1, -1):
            if DRBG_ctx.V[j] == 0xFF:
                DRBG_ctx.V[j] = 0x00
            else:
                DRBG_ctx.V[j] += 1
                break

        AES256_ECB(DRBG_ctx.Key, DRBG_ctx.V, block)

        if xlen > 15:
            x[i : i + 16] = block
            i += 16
            xlen -= 16
        else:
            x[i : i + xlen] = block[:xlen]
            xlen = 0

    AES256_CTR_DRBG_Update(None, DRBG_ctx.Key, DRBG_ctx.V)
    DRBG_ctx.reseed_counter += 1

    return RNG_SUCCESS


def AES256_CTR_DRBG_Update(provided_data, Key, V):
    temp = bytearray(48)

    for i in range(3):
        for j in range(15, -1, -1):
            if V[j] == 0xFF:
                V[j] = 0x00
            else:
                V[j] += 1
                break

        temp_view = memoryview(temp)[16 * i : 16 * (i + 1)]
        AES256_ECB(Key, V, temp_view)

    if provided_data:
        temp = bytearray([temp[i] ^ provided_data[i] for i in range(48)])

    Key[:] = temp[:32]
    V[:] = temp[32:48]
