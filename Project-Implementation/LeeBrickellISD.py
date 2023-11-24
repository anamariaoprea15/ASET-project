import Tools
import numpy as np
	
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
        self.tools = Tools()
        self._observers = []

    def integer_to_combination(self, j):
        pass

    def is_extract(self, H, syndrome):
        # Perform the extract operation
        # Notify observers after the extract operation
        result = self.extract(H, syndrome)
        self.notify_observers(result)
        
    def attack(self):
        inner_iter_counts = []
        outer_iter_count = 0

        while True:
            try:
                P, V, U, inner_iteration_count = self.inner_loop()
            except:
                raise Exception("Exiting ISD algorithm, maximum iterations exceeded in inner loop")

            inner_iter_counts.append(inner_iteration_count)
            r, n = self.tools.H.shape
            k = n - r
            s_curr = U * self.tools.syndrome
            s_curr = s_curr.transpose().list()

            for j in range(k):  # ajustare pentru a evita utilizarea itertools
                i = self.integer_to_combination(j)
                s_curr = np.add(V.column(i), s_curr)

                if self.tools.get_array_weight(s_curr) == self.tools.t - IDEAL_P:
                    e_curr = [0] * k + s_curr.tolist()
                    for i in range(len(j)):
                        to_add = [0] * i + [1] + [0] * (r + k - 1 - i)
                        e_curr = np.add(e_curr, to_add)

                    if self.tools.is_of_desired_weight(e_curr, self.tools.t):
                        result = np.dot(np.matrix(e_curr), P.T)
                        if np.dot(self.tools.H, result.transpose()) == self.tools.syndrome:
                            return result, outer_iter_count, np.mean(inner_iter_counts)

                    if outer_iter_count > MAX_ITERATIONS_OUTER:
                        raise Exception("Maximum iterations exceeded in outer loop")

            outer_iter_count += 1
            print("Running outer iteration number %d" % outer_iter_count)

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
    tools = Tools(4, 8, 2, [0, 1, 0, 1, 1, 0, 1, 0])
    lee_brickell_isd_instance = LeeBrickellISD(tools)
    extract_observer = ExtractObserver()

    lee_brickell_isd_instance.subscribe(extract_observer)
    
    # Simulate the extract operation
    H = np.array([[1, 0, 1, 0],
                  [0, 1, 1, 1],
                  [1, 1, 0, 0]])
    syndrome = np.array([1, 0, 1, 1])

    lee_brickell_isd_instance.is_extract(H, syndrome)
