def recon(v, c, d):
    """
    Reconstructs the vector `v` based on vectors `c` and `d`.
    
    Args:
        v (list of int): The output vector to store the reconstructed values.
        c (list of int): The vector of coefficients.
        d (list of int): The decision vector, each element should be 0 or 1.
    """
    for i in range(256):
        if d[i] == 0:
            v[i] = c[i] - 1024
        else:
            v[i] = c[i] + 1024

# Example usage:
if __name__ == "__main__":
    c = [1500] * 256  # Example coefficient vector
    d = [0, 1] * 128  # Example decision vector
    v = [0] * 256     # Output vector
    recon(v, c, d)
    print(v)

