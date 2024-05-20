# SABER_indcpa.py
import numpy as np
from SABER_params import SABER_L, SABER_N, SABER_Q, SABER_ET
from cbd import cbd  # Simulates error distribution
from poly_mul import poly_mul  # Simulates polynomial multiplication

def generate_noise(size):
    noise = np.zeros(size, dtype=int)
    random_bytes = []
    for x in range(size[0]):
    	random_bytes.append(np.random.bytes(size[1] * 3))  # Assuming 3 bytes per noise sample
    cbd(noise, random_bytes)
    return noise

def indcpa_keypair():
    A = np.random.randint(0, SABER_Q, (SABER_L, SABER_L, SABER_N))
    s = generate_noise((SABER_L, SABER_N))
    e = generate_noise((SABER_L, SABER_N))
    b = (poly_mul(A, s) + e) % SABER_Q
    pk = (A, b)
    sk = s
    return pk, sk

def indcpa_enc(pk, message):
    A, b = pk
    r = generate_noise((SABER_L, SABER_N))
    e = generate_noise(SABER_N)
    u = (poly_mul(A, r) + e) % SABER_Q
    v = (poly_mul(b, r) + message) % SABER_Q  # Assume message is processed to fit
    return u, v

def indcpa_dec(sk, u, v):
    rec = (poly_mul(u, sk) % SABER_Q)
    message_decoded = (v - rec) % SABER_Q
    return message_decoded

