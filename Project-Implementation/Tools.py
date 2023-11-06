import numpy as np

class Tools:
    def __init__(self, r, n, t, syndrome):
        self.H = np.empty((r, n))
        self.t = t
        self._syndrome = syndrome
        self._observers = []

    @property
    def syndrome(self):
        return self._syndrome

    @syndrome.setter
    def syndrome(self, new_syndrome):
        if new_syndrome != self._syndrome:
            self._syndrome = new_syndrome
            self.notify_observers()

    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)

    def generate_random_permutation(self, n):
        """
        Returns a random permutation matrix
        """
        pass

    def weight(self, e):
        """
        Returns the weight of the error vector
        """
        pass

    def reduced_row_echelon_form(self, H):
        """
        Computes the reduced row echelon form of the matrix H
        """
        pass

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
