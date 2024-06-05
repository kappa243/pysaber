def verify(a, b, len):
    """
    Compare two byte strings in constant time.

    Parameters:
    a (bytes): The first byte string to compare.
    b (bytes): The second byte string to compare.
    len (int): The length of the byte strings to compare.

    Returns:
    int: 0 if the byte strings are equal, 1 otherwise.
    """
    result = 0
    for i in range(len):
        result |= a[i] ^ b[i]
    return (1 & ((result - 1) >> 8))



def cmov(r, x, len, b):
    """
    Conditional move.

    Parameters:
    r (bytearray): The resulting byte string.
    x (bytes): The byte string to move.
    len (int): The length of the byte strings to compare.
    b (int): The condition to move x to r.
    """
    b = -b
    for i in range(len):
        r[i] ^= b & (x[i] ^ r[i])