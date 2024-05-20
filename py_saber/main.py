from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from SABER_indcpa import indcpa_keypair, indcpa_enc, indcpa_dec
import numpy as np

def aes_encrypt(key, plaintext):
    """Encrypts plaintext using AES."""
    backend = default_backend()
    iv = os.urandom(16)  # AES block size is 16 bytes
    cipher = Cipher(algorithms.AES(key[:32]), modes.CFB(iv), backend=backend)  # Use first 32 bytes of key for AES-256
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return iv, ciphertext

def aes_decrypt(key, iv, ciphertext):
    """Decrypts ciphertext using AES."""
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key[:32]), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()

def main():
    # SABER KEM to exchange keys
    pk, sk = indcpa_keypair()
    message = "Secure message using SABER and AES!"
    
    # SABER encapsulation to generate and exchange a secret key
    ciphertext_kem, ss_encapsulated = indcpa_enc(pk)
    
    # AES encryption using the encapsulated secret key
    iv, encrypted_message = aes_encrypt(ss_encapsulated, message)
    
    # SABER decapsulation to recover the secret key
    ss_decapsulated = indcpa_dec(sk, ciphertext_kem)
    
    # AES decryption using the decapsulated secret key
    decrypted_message = aes_decrypt(ss_decapsulated, iv, encrypted_message)
    
    print("Original Message:", message)
    print("Encrypted Message (AES):", encrypted_message)
    print("Decrypted Message:", decrypted_message)

if __name__ == "__main__":
    main()

