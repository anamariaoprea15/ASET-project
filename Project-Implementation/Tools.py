import random
import numpy as np

def log_syndrome_update(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        args[0].notify_observers()  # Notify observers after the update
        return result

    return wrapper

def log_random_permutation(func):
    pass
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        args[0].notify_observers()  # Notify observers after generating a random permutation
        return result

    return wrapper

class Tools:
    def __init__(self, r, n, t, syndrome):
        self.H = np.empty((r, n))
        self.t = t
        self._syndrome = syndrome
        self._observers = []

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
        Computes the reduced row echelon form of the matrix H
        """
        lead = 0
        rows, cols = H.shape

        for r in range(rows):
            if lead >= cols:
                return H

            i = r
            while H[i, lead] == 0:
                i += 1
                if i == rows:
                    i = r
                    lead += 1
                    if cols == lead:
                        return H

            # Swap rows
            H[[i, r], :] = H[[r, i], :]

            # Scale the pivot row
            scale = H[r, lead]
            H[r, :] = H[r, :] / float(scale)

            # Eliminate other rows
            for i in range(rows):
                if i != r:
                    scale = H[i, lead]
                    H[i, :] = H[i, :] - H[r, :] * scale

            lead += 1

        return H

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
