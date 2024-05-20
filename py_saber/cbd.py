def load24(x):
    """
    Loads 3 bytes and returns them as a 24-bit integer.
    
    Args:
        x (bytes): A bytes object of length 3.
        
    Returns:
        int: The 24-bit integer representation of the input bytes.
    """
    r = x[0]
    r |= x[1] << 8
    r |= x[2] << 16
    return r

def cbd(r, buf):
    """
    Component-wise bounded distribution generator.
    Args:
        r (list of int): Output vector to store the generated noise.
        buf (bytes): Input buffer of bytes, used to derive the noise.
    """
    n = len(r)
    if len(buf) < 3 * n:
        raise ValueError("Buffer too small for the number of elements")
    
    for i in range(n):
        t = load24(buf[3 * i:3 * i + 3])
        d = t & 0x555555
        d += (t >> 1) & 0x555555
        a = d & 0xff
        b = (d >> 8) & 0xff
        r[i] = a - b


# Example usage:
if __name__ == "__main__":
    r = [0] * 256
    buf = bytes([0x01, 0x23, 0x45] * 256)  # Example buffer
    cbd(r, buf)
    print(r)

