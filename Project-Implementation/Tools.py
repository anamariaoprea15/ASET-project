import numpy as np
class Tools:
    syndrome = [] # the syndrome vector
    H = np.empty(()) # binary parity check matrix
    P = np.empty(()) # n x n permutation matrix
    t = int() # the weight of the error vector to be recovered
    def __init__(self, r, n, t, syndrome): # r and n are the dimensions of H
        self.H = np.empty((r, n))
        self.t = t
        self.syndrome = syndrome

    def generate_random_permutation(n):
        """
        Returns a random permutation matrix
        """
        pass

    def weight(e):
        """
        Returns the weight of the error vector
        """
        pass

    def reduced_row_echelon_form(H):
        """
        Computes the reduced row echelon form of the matrix H
        """
        pass
