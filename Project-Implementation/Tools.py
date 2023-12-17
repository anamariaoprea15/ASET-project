import numpy as np
from functools import wraps
import logging
import time
from pprint import pprint

# Configure the logging system
def configure_logging():
    if not logging.getLogger().handlers:
        logging.basicConfig(filename='monitoring.log', level=logging.DEBUG)

configure_logging()

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        logging.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
        return result

    return wrapper

def log_random_permutation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logging.info("Random permutation generated.")
        return result

    return wrapper

def log_syndrome_update(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        old_syndrome = args[0].syndrome  # Get the current syndrome before the update
        result = func(*args, **kwargs)
        new_syndrome = args[0].syndrome  # Get the updated syndrome

        # Check if the syndrome has changed before logging
        if old_syndrome != new_syndrome:
            args[0].notify_observers()  # Notify observers after the update
            logging.info(f"Syndrome has been updated: {new_syndrome}")
        return result

    return wrapper

class Tools:
    def __init__(self, k, n, t, syndrome):
        self.k = k
        self.n = n
        self.r = n - k
        self.H = np.empty((self.r, n))
        self.t = t
        self._syndrome = syndrome
        self._observers = []
        logging.info(f"Initial syndrome: {self._syndrome}") # Log the initial syndrome

    @property
    def state(self):
        return {
            "k": self.k,
            "n": self.n,
            "r": self.r,
            "t": self.t,
            "syndrome": self.syndrome,
            #"syndrome": np.array(self.syndrome).tolist(),  # Convert to list if self.syndrome is a NumPy array
        }

    def get_parameters(self):
        return self.k, self.n, self.r, self.t, self.syndrome

    @property
    def syndrome(self):
        return self._syndrome

    @syndrome.setter
    @log_syndrome_update
    def syndrome(self, new_syndrome):
        if new_syndrome != self._syndrome:
            self._syndrome = new_syndrome
            self.notify_observers()

    @log_execution_time
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
        try:
            #result = 1 / 0 # Simulate an error by dividing by zero
            old_syndrome = self.syndrome.copy()  # Save the current syndrome before the update

            positions = np.arange(n)
            np.random.shuffle(positions)

            result = np.eye(n, dtype=int)[positions]
            print("Random permutation generated.")  # Just for testing 
            print(result)

         # Check if the syndrome has changed before notifying observers
            if old_syndrome != self.syndrome:
                self.notify_observers()

            return result
        
        except ValueError as ve:
            logging.error(f"ValueError in generating random permutation: {ve}")
            raise
        except Exception as e:
            logging.exception("Error in generating random permutation")

    def weight(self, e):
        """
        Returns the weight of the error vector
        """
        return np.linalg.norm(e, ord=0)

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
        lead = 0  # initial lead position
        rows, cols = H.shape  # dimensions of H
        
        max_dimension = max(rows, cols)
        P = np.identity(max_dimension)  # Initialize P as the identity matrix

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

    state_info = tools.state
    pprint(state_info)