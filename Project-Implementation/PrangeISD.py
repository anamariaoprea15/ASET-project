import Tools
import numpy as np
from numpy import linalg

class PrangeISD:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PrangeISD, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        """
        Instantiates the Prange class
        """
        self.tools = Tools()
        self._observers = []

    def attack(self):
        # Perform the Prange attack algorithm
        # Notify observers after the attack operation
        result = self.perform_attack()
        self.notify_observers(result)

    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, result):
        for observer in self._observers:
            observer.update(result)

    def perform_attack(self):
        # Simulate the Prange attack operation
        result = "Simulated attack result"
        k,n,r,t,syndrome = Tools.get_parameters()
        while True: # outer loop, while weight error is not t
            while True:
                P = Tools.generate_random_permuationt(n)
                H_prim = np.dot(H,P) # H * P
                T = H_prim[:, n-k:n] # obtinut din H_prim = (K|T), unde T (n-k)x(n-k)
                # check rank(T) != n - k => then go back to permutation
                if linalg.matrix_rank(T) == r:
                     break 
            # apply elementary row operations to Hp to get RREF
            #  R * H_prim = (Q|I_n-k)
            H, R = Tools.reduced_row_echelon_form(H_prim) # de mofiicat
        
            syndrome = np.dot(R,syndrome)
        
            if Tools.weight(syndrome) == t:
                epsi = np.zeros((k, 1))
                error = np.append(epsi, syndrome)
            
                return np.dot(P, error) #P*e,  end of algorithm 
        

        

# Define an observer class
class AttackObserver:
    def update(self, result):
        # Handle the update from the attack operation
        print("Attack operation result:", result)

# Usage:
if __name__ == "__main__":
    prange_isd_instance = PrangeISD()
    attack_observer = AttackObserver()
    
    prange_isd_instance.subscribe(attack_observer)
    
    # Simulate the attack operation
    prange_isd_instance.attack()
