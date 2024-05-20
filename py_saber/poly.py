class Poly:
    """
    Class representing a polynomial with coefficients.

    Attributes:
        coeffs (list of int): The coefficients of the polynomial.
    """
    def __init__(self):
        self.coeffs = [0] * 256

def poly_add(res, a, b):
    """
    Adds two polynomials and stores the result in another polynomial object.

    Args:
        res (Poly): The polynomial object to store the result.
        a (Poly): The first polynomial to add.
        b (Poly): The second polynomial to add.
    """
    for i in range(256):
        res.coeffs[i] = (a.coeffs[i] + b.coeffs[i]) % 65536

# Example usage:
if __name__ == "__main__":
    poly1 = Poly()
    poly2 = Poly()
    poly1.coeffs = [1] * 256
    poly2.coeffs = [2] * 256
    result_poly = Poly()
    poly_add(result_poly, poly1, poly2)
    print(result_poly.coeffs)

