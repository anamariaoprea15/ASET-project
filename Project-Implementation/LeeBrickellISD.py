import Tools
import numpy as np
import random
from numpy import linalg
	
MAX_ITERATIONS_INNER = 1000
MAX_ITERATIONS_OUTER = 100000
IDEAL_P = 2


class LeeBrickellISD:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LeeBrickellISD, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        """
        Instantiates the Lee-Brickell class
        """
        self.tools = Tools.Tools(4, 8, 2, [0, 1, 0, 1, 1, 0, 1, 0])
        self._observers = []

    def integer_to_combination(self, j):
        """
        Converts an integer j into a set of p distinct integers in {0, ..., k-1}.
        """
        k = self.tools.n - self.tools.r  # Computes k based on the dimensions of the H matrix
        p = IDEAL_P

        combination = set()
        remaining_numbers = list(range(k))

        while len(combination) < p:
            selected_index = random.choice(remaining_numbers)
            combination.add(selected_index)
            remaining_numbers.remove(selected_index)

        return combination
   
    def is_desired_weight(self, e, t):
        """
        Checks if the weight of the error vector e is equal to the desired weight t.
        """
        return self.tools.weight(e) == t
    
    def is_extract(self, H, syndrome):
        # Perform the extract operation
        # Notify observers after the extract operation
        result = self.extract(H, syndrome)
        self.notify_observers(result)
        
       
    def attack(self):
        k, n, r, t, syndrome = Tools.get_parameters()

        while True:
            while True:
                P = Tools.generate_random_permutation(n)
                H_prim = np.dot(self.H, P)
                T = H_prim[:, n - k:n]

                # check rank(T) != n - k 
                if linalg.matrix_rank(T) == r:
                    break
                
            R = self.reduced_row_echelon_form(H_prim)
            syndrome = np.dot(R, syndrome)

            # Lee-Brickell specific steps
            #For small p, pick p of the k columns on the left, compute their sum Xp
            for p in range(1, t + 1):
                # Choose p of the k columns on the left, compute their sum Xp
                selected_columns = np.random.choice(range(k), p, replace=False)
                Xp = np.sum(H_prim[:, selected_columns], axis=1)

                # Check if wt(s_0 + Xp) == t - p
                if self.weight(syndrome + Xp) == t - p:
                    e_prim = np.concatenate((np.zeros((k, 1)), syndrome + Xp))
                    return np.dot(P, e_prim)      


    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, result):
        for observer in self._observers:
            observer.update(result)

    def extract(self, H, syndrome):
        # Simulate the extract operation
        result = "Simulated extraction result"
        return result

# Define an observer class
class ExtractObserver:
    def update(self, result):
        # Handle the update from the extract operation
        print("Extract operation result:", result)

# Usage:
if __name__ == "__main__":
    tools = Tools.Tools(4, 8, 2, [0, 1, 0, 1, 1, 0, 1, 0])
    lee_brickell_isd_instance = LeeBrickellISD(tools)
    extract_observer = ExtractObserver()

    lee_brickell_isd_instance.subscribe(extract_observer)
    
    # Simulate the extract operation
    H = np.array([[1, 0, 1, 0],
                  [0, 1, 1, 1],
                  [1, 1, 0, 0]])
    syndrome = np.array([1, 0, 1, 1])

    lee_brickell_isd_instance.attack()
