import numpy as np
class Poly:
    """
    Represents a polynomial with 256 coefficients.
    """
    def __init__(self, coeffs):
        self.coeffs = np.array(coeffs)

def poly_mul(A, s):
    """
    Multiplies polynomial matrix A with polynomial vector s.
    Args:
        A (numpy.ndarray): The polynomial matrix of dimensions (L, L, N).
        s (numpy.ndarray): The polynomial vector of dimensions (L, N).
    Returns:
        numpy.ndarray: The result of the polynomial multiplication, dimensions (L, N).
    """
    L, _, N = A.shape
    result = np.zeros((L, N), dtype=int)
    for i in range(L):
        for j in range(L):
            for k in range(N):
                for l in range(N):
                    result[i, (k + l) % N] += A[i, j, k] * s[j, l]
    return result % SABER_Q

# Example usage:
if __name__ == "__main__":
    poly1 = Poly()
    poly2 = Poly()
    poly1.coeffs = [1] * 256
    poly2.coeffs = [2] * 256
    result_poly = Poly()
    poly_mul(result_poly, poly1, poly2)
    print(result_poly.coeffs)

