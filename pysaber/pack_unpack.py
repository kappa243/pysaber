# For further context refer to section 8.2.7 of documentation

from pysaber.saber_params import (SABER_EP, SABER_ET, SABER_KEYBYTES, SABER_L,
                                  SABER_N, SABER_POLYBYTES)

def POLT2BS(bytes, data):
    """
    Converts polynomial coefficients to byte representation based on SABER_ET parameter.
    
    Args:
        bytes (bytearray): The byte array to store the converted data.
        data (list): The list of polynomial coefficients.
    """
    if SABER_ET == 3:
        for j in range(SABER_N // 8):
            offset_byte = 3 * j
            offset_data = 8 * j
            bytes[offset_byte] = (
                (data[offset_data] & 0x07)
                | ((data[offset_data + 1] & 0x07) << 3)
                | ((data[offset_data + 2] & 0x03) << 6)
            )
            bytes[offset_byte + 1] = (
                ((data[offset_data + 2] >> 2) & 0x01)
                | ((data[offset_data + 3] & 0x07) << 1)
                | ((data[offset_data + 4] & 0x07) << 4)
                | ((data[offset_data + 5] & 0x01) << 7)
            )
            bytes[offset_byte + 2] = (
                ((data[offset_data + 5] >> 1) & 0x03)
                | ((data[offset_data + 6] & 0x07) << 2)
                | ((data[offset_data + 7] & 0x07) << 5)
            )
    elif SABER_ET == 4:
        for j in range(SABER_N // 2):
            offset_byte = j
            offset_data = 2 * j
            bytes[offset_byte] = (data[offset_data] & 0x0F) | ((data[offset_data + 1] & 0x0F) << 4)
    elif SABER_ET == 6:
        for j in range(SABER_N // 4):
            offset_byte = 3 * j
            offset_data = 4 * j
            bytes[offset_byte] = (data[offset_data] & 0x3F) | ((data[offset_data + 1] & 0x03) << 6)
            bytes[offset_byte + 1] = ((data[offset_data + 1] >> 2) & 0x0F) | ((data[offset_data + 2] & 0x0F) << 4)
            bytes[offset_byte + 2] = ((data[offset_data + 2] >> 4) & 0x03) | ((data[offset_data + 3] & 0x3F) << 2)
    else:
        raise ValueError("Unsupported SABER parameter.")

def BS2POLT(bytes, data):
    """
    Converts byte representation back to polynomial coefficients based on SABER_ET parameter.
    
    Args:
        bytes (bytearray): The byte array containing the data to be converted.
        data (list): The list to store the polynomial coefficients.
    """
    if SABER_ET == 3:
        for j in range(SABER_N // 8):
            offset_byte = 3 * j
            offset_data = 8 * j
            data[offset_data] = bytes[offset_byte] & 0x07
            data[offset_data + 1] = (bytes[offset_byte] >> 3) & 0x07
            data[offset_data + 2] = ((bytes[offset_byte] >> 6) & 0x03) | ((bytes[offset_byte + 1] & 0x01) << 2)
            data[offset_data + 3] = (bytes[offset_byte + 1] >> 1) & 0x07
            data[offset_data + 4] = (bytes[offset_byte + 1] >> 4) & 0x07
            data[offset_data + 5] = ((bytes[offset_byte + 1] >> 7) & 0x01) | ((bytes[offset_byte + 2] & 0x03) << 1)
            data[offset_data + 6] = (bytes[offset_byte + 2] >> 2) & 0x07
            data[offset_data + 7] = (bytes[offset_byte + 2] >> 5) & 0x07
    elif SABER_ET == 4:
        for j in range(SABER_N // 2):
            offset_byte = j
            offset_data = 2 * j
            data[offset_data] = bytes[offset_byte] & 0x0F
            data[offset_data + 1] = (bytes[offset_byte] >> 4) & 0x0F
    elif SABER_ET == 6:
        for j in range(SABER_N // 4):
            offset_byte = 3 * j
            offset_data = 4 * j
            data[offset_data] = bytes[offset_byte] & 0x3F
            data[offset_data + 1] = ((bytes[offset_byte] >> 6) & 0x03) | ((bytes[offset_byte + 1] & 0x0F) << 2)
            data[offset_data + 2] = ((bytes[offset_byte + 1] >> 4) & 0x0F) | ((bytes[offset_byte + 2] & 0x03) << 4)
            data[offset_data + 3] = (bytes[offset_byte + 2] >> 2) & 0x3F
    else:
        raise ValueError("Unsupported SABER parameter.")

def POLq2BS(bytes, data):
    """
    Converts polynomial coefficients to byte representation for SABER_q.
    
    Args:
        bytes (bytearray): The byte array to store the converted data.
        data (list): The list of polynomial coefficients.
    """
    for j in range(SABER_N // 8):
        offset_byte = 13 * j
        offset_data = 8 * j
        bytes[offset_byte] = data[offset_data] & 0xFF
        bytes[offset_byte + 1] = ((data[offset_data] >> 8) & 0x1F) | ((data[offset_data + 1] & 0x07) << 5)
        bytes[offset_byte + 2] = (data[offset_data + 1] >> 3) & 0xFF
        bytes[offset_byte + 3] = ((data[offset_data + 1] >> 11) & 0x03) | ((data[offset_data + 2] & 0x3F) << 2)
        bytes[offset_byte + 4] = ((data[offset_data + 2] >> 6) & 0x7F) | ((data[offset_data + 3] & 0x01) << 7)
        bytes[offset_byte + 5] = (data[offset_data + 3] >> 1) & 0xFF
        bytes[offset_byte + 6] = ((data[offset_data + 3] >> 9) & 0x0F) | ((data[offset_data + 4] & 0x0F) << 4)
        bytes[offset_byte + 7] = (data[offset_data + 4] >> 4) & 0xFF
        bytes[offset_byte + 8] = ((data[offset_data + 4] >> 12) & 0x01) | ((data[offset_data + 5] & 0x7F) << 1)
        bytes[offset_byte + 9] = (data[offset_data + 5] >> 7) & 0x3F | ((data[offset_data + 6] & 0x03) << 6)
        bytes[offset_byte + 10] = (data[offset_data + 6] >> 2) & 0xFF
        bytes[offset_byte + 11] = ((data[offset_data + 6] >> 10) & 0x07) | ((data[offset_data + 7] & 0x1F) << 3)
        bytes[offset_byte + 12] = (data[offset_data + 7] >> 5) & 0xFF

def BS2POLq(bytes, data):
    """
    Converts byte representation back to polynomial coefficients for SABER_q.
    
    Args:
        bytes (bytearray): The byte array containing the data to be converted.
        data (list): The list to store the polynomial coefficients.
    """
    for j in range(SABER_N // 8):
        offset_byte = 13 * j
        offset_data = 8 * j
        data[offset_data] = (bytes[offset_byte] & 0xFF) | ((bytes[offset_byte + 1] & 0x1F) << 8)
        data[offset_data + 1] = (
            ((bytes[offset_byte + 1] >> 5) & 0x07)
            | ((bytes[offset_byte + 2] & 0xFF) << 3)
            | ((bytes[offset_byte + 3] & 0x03) << 11)
        )
        data[offset_data + 2] = (bytes[offset_byte + 3] >> 2 & 0x3F) | ((bytes[offset_byte + 4] & 0x7F) << 6)
        data[offset_data + 3] = (
            (bytes[offset_byte + 4] >> 7 & 0x01)
            | ((bytes[offset_byte + 5] & 0xFF) << 1)
            | ((bytes[offset_byte + 6] & 0x0F) << 9)
        )
        data[offset_data + 4] = (
            (bytes[offset_byte + 6] >> 4 & 0x0F)
            | ((bytes[offset_byte + 7] & 0xFF) << 4)
            | ((bytes[offset_byte + 8] & 0x01) << 12)
        )
        data[offset_data + 5] = (bytes[offset_byte + 8] >> 1 & 0x7F) | ((bytes[offset_byte + 9] & 0x3F) << 7)
        data[offset_data + 6] = (
            (bytes[offset_byte + 9] >> 6 & 0x03)
            | ((bytes[offset_byte + 10] & 0xFF) << 2)
            | ((bytes[offset_byte + 11] & 0x07) << 10)
        )
        data[offset_data + 7] = (bytes[offset_byte + 11] >> 3 & 0x1F) | ((bytes[offset_byte + 12] & 0xFF) << 5)

def POLp2BS(bytes, data):
    """
    Converts polynomial coefficients to byte representation for SABER_p.
    
    Args:
        bytes (bytearray): The byte array to store the converted data.
        data (list): The list of polynomial coefficients.
    """
    for j in range(SABER_N // 4):
        offset_byte = 5 * j
        offset_data = 4 * j
        bytes[offset_byte] = data[offset_data] & 0xFF
        bytes[offset_byte + 1] = ((data[offset_data] >> 8) & 0x03) | ((data[offset_data + 1] & 0xFF) << 2)
        bytes[offset_byte + 2] = ((data[offset_data + 1] >> 6) & 0x0F) | ((data[offset_data + 2] & 0xFF) << 4)
        bytes[offset_byte + 3] = ((data[offset_data + 2] >> 4) & 0x3F) | ((data[offset_data + 3] & 0xFF) << 6)
        bytes[offset_byte + 4] = (data[offset_data + 3] >> 2) & 0xFF

def BS2POLp(bytes, data):
    """
    Converts byte representation back to polynomial coefficients for SABER_p.
    
    Args:
        bytes (bytearray): The byte array containing the data to be converted.
        data (list): The list to store the polynomial coefficients.
    """
    for j in range(SABER_N // 4):
        offset_byte = 5 * j
        offset_data = 4 * j
        data[offset_data] = (bytes[offset_byte] & 0xFF) | ((bytes[offset_byte + 1] & 0x03) << 8)
        data[offset_data + 1] = (bytes[offset_byte + 1] >> 2 & 0xFF) | ((bytes[offset_byte + 2] & 0x0F) << 6)
        data[offset_data + 2] = (bytes[offset_byte + 2] >> 4 & 0xFF) | ((bytes[offset_byte + 3] & 0x3F) << 4)
        data[offset_data + 3] = (bytes[offset_byte + 3] >> 6 & 0xFF) | ((bytes[offset_byte + 4] & 0xFF) << 2)

def POLVECq2BS(bytes, data):
    """
    Converts vector of polynomial coefficients to byte representation for SABER_q.
    
    Args:
        bytes (bytearray): The byte array to store the converted data.
        data (list of lists): The list of polynomial coefficient vectors.
    """
    for i in range(SABER_L):
        POLq2BS(bytes[i * SABER_POLYBYTES:], data[i])

def BS2POLVECq(bytes, data):
    """
    Converts byte representation back to vector of polynomial coefficients for SABER_q.
    
    Args:
        bytes (bytearray): The byte array containing the data to be converted.
        data (list of lists): The list to store the polynomial coefficient vectors.
    """
    for i in range(SABER_L):
        BS2POLq(bytes[i * SABER_POLYBYTES:], data[i])

def POLVECp2BS(bytes, data):
    """
    Converts vector of polynomial coefficients to byte representation for SABER_p.
    
    Args:
        bytes (bytearray): The byte array to store the converted data.
        data (list of lists): The list of polynomial coefficient vectors.
    """
    for i in range(SABER_L):
        POLp2BS(bytes[i * (SABER_EP * SABER_N // 8):], data[i])

def BS2POLVECp(bytes, data):
    """
    Converts byte representation back to vector of polynomial coefficients for SABER_p.
    
    Args:
        bytes (bytearray): The byte array containing the data to be converted.
        data (list of lists): The list to store the polynomial coefficient vectors.
    """
    for i in range(SABER_L):
        BS2POLp(bytes[i * (SABER_EP * SABER_N // 8):], data[i])

def BS2POLmsg(bytes, data):
    """
    Converts byte representation back to polynomial message coefficients.
    
    Args:
        bytes (bytearray): The byte array containing the data to be converted.
        data (list): The list to store the polynomial message coefficients.
    """
    for j in range(SABER_KEYBYTES):
        for i in range(8):
            data[j * 8 + i] = (bytes[j] >> i) & 0x01

def POLmsg2BS(bytes, data):
    """
    Converts polynomial message coefficients to byte representation.
    
    Args:
        bytes (bytearray): The byte array to store the converted data.
        data (list): The list of polynomial message coefficients.
    """
    bytes.fill(0)
    for j in range(SABER_KEYBYTES):
        for i in range(8):
            bytes[j] |= (data[j * 8 + i] & 0x01) << i
