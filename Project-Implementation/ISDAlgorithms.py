import PrangeISD
import LeeBrickellISD

def log_state_change(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        print(f"State changed to: {self.state}")
        return result

    return wrapper

class ISDAlgorithms:
    def __init__(self):
        self.lee_brickel_isd = LeeBrickellISD.LeeBrickellISD()
        self.Prange_isd = PrangeISD.PrangeISD()
        self.state = 'Idle'  # Initial state
        print("The application has started!")

    @log_state_change
    def change_state(self, new_state):
        self.state = new_state

    @log_state_change
    def complexity_analysis(self):
        if self.state == 'Idle':
            print("Starting complexity analysis...")
            # Perform complexity analysis logic
            # Transition to ComplexityAnalysis state if needed
            self.change_state('ComplexityAnalysis')
        elif self.state == 'ComplexityAnalysis':
            print("Already performing complexity analysis...")
        else:
            print("Invalid state")

    # Add more methods for other states and transitions as needed

if __name__ == "__main__":
    isd_instance = ISDAlgorithms()
    isd_instance.complexity_analysis()
    isd_instance.change_state('NewState')
