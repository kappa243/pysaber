def pack(out, in_, len_):
    """
    Packs a list of uint16_t integers into a byte array.
    
    Args:
        out (bytearray): The bytearray to store the packed bytes.
        in_ (list): The list of integers to pack.
        len_ (int): The number of integers in the list to pack.
    """
    for i in range(len_):
        out[2 * i] = in_[i] & 0xFF
        out[2 * i + 1] = (in_[i] >> 8) & 0xFF

def unpack(out, in_, len_):
    """
    Unpacks a bytearray into a list of uint16_t integers.
    
    Args:
        out (list): The list to store the unpacked integers.
        in_ (bytearray): The bytearray containing the packed integers.
        len_ (int): The number of integers to unpack.
    """
    for i in range(len_):
        out[i] = in_[2 * i] | (in_[2 * i + 1] << 8)

# Example usage:
if __name__ == "__main__":
    in_numbers = [1025, 2049, 4097]
    out_bytes = bytearray(2 * len(in_numbers))
    pack(out_bytes, in_numbers, len(in_numbers))
    print(list(out_bytes))

    unpacked_numbers = [0] * len(in_numbers)
    unpack(unpacked_numbers, out_bytes, len(in_numbers))
    print(unpacked_numbers)

