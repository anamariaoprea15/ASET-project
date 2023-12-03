import random
import numpy as np

def log_syndrome_update(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        args[0].notify_observers()  # Notify observers after the update
        return result

    return wrapper

def log_random_permutation(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        args[0].notify_observers()  # Notify observers after generating a random permutation
        return result

    return wrapper

class Tools:
    def __init__(self, k, n, t, syndrome):
        self.r = n - k
        self.H = np.empty((self.r, n))
        self.t = t
        self._syndrome = syndrome
        self._observers = []
    
    def get_parameters(self):
        return self.k, self.n, self.r, self.t, self.syndrome

    @property
    @log_syndrome_update
    def syndrome(self):
        return self._syndrome

    @syndrome.setter
    @log_syndrome_update
    def syndrome(self, new_syndrome):
        if new_syndrome != self._syndrome:
            self._syndrome = new_syndrome

    @log_random_permutation
    def generate_random_permutation(self, n):
        """
        Returns a random permutation matrix

        For line permutation:
            The column index will tell which line will be moved. The position of the '1'
            on the column will tell the new position of said line. The matrix will be multiplied
            from the left. (Ex: P x H)

        For column permutation:
            The line index will tell which column will be moved. The position of the '1'
            on the line will tell the new position of said column. The matrix will be multiplied
            from the right. (Ex: H x P)
        """
        result = np.zeros([n, n], dtype=int)
        positions = [i for i in range(n)]  # [0, 1, 2, ..., n-1]
        random.shuffle(positions)

        for i in positions:
            result[i][positions[i]] = 1
        print(result)
        return result

    def weight(self, e): # tested
        """
        Returns the weight of the error vector
        """
        w = 0
        for digit in e:
            if digit != 0:
                w += 1
        return w

    def reduced_row_echelon_form(self, H):
        """
        Computes and returns the reduced row echelon form of the matrix H
        and the transformation matrix P, such that H x P = RREF(H)

        P gets initialized as the identity matrix, so H x P = H
        Using a lead index, we iterate through H and swap each row with the first row met beneath
        (or itself) that does not have the value 0 in the lead position. Afterwards, we scale the
        given row r, dividing it by the lead value, and subtract the initial value of the row from
        the other rows.

        Every change that gets applied to H will be applied to P respectively, so as to obtain
        the transformation matrix P needed.
        """
        lead = 0 # initial lead position
        rows, cols = H.shape # dimensions of H
        P = np.identity(cols)  # Initialize P as the identity matrix

        for r in range(rows):
            if lead >= cols:
                return H, P

            i = r
            while H[i, lead] == 0:
                i += 1
                if i == rows:
                    i = r
                    lead += 1
                    if cols == lead:
                        return H, P

            # Swap rows in both H and P
            H[[i, r], :] = H[[r, i], :]
            P[[i, r], :] = P[[r, i], :]

            # Scale the pivot row
            scale = H[r, lead]
            H[r, :] = H[r, :] / float(scale)
            P[r, :] = P[r, :] / float(scale)

            # Subtract from other rows
            for i in range(rows):
                if i != r:
                    scale = H[i, lead]
                    H[i, :] = H[i, :] - H[r, :] * scale
                    P[i, :] = P[i, :] - P[r, :] * scale

            lead += 1

        return H, P


    def subscribe(self, observer): 
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)

class SyndromeObserver:
    def update(self, tools):
        # Handle the updated syndrome
        print("Syndrome has been updated:", tools.syndrome)

# Usage example:
if __name__ == "__main__":
    syndrome_observer = SyndromeObserver()

    tools = Tools(4, 8, 2, [0, 1, 0, 1, 1, 0, 1, 0])
    tools.subscribe(syndrome_observer)

    # Simulate an update in the syndrome
    tools.syndrome = [1, 0, 1, 1, 0, 0, 0, 1]

    # Simulate generating a random permutation
    tools.generate_random_permutation(4)