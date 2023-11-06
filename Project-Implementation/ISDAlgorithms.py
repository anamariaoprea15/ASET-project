import PrangeISD
import LeeBrickellISD

class ISDAlgorithms:
    def __init__(self):
        self.lee_brickel_isd = LeeBrickellISD()
        self.Prange_isd = PrangeISD()
        self.state = 'Idle'  # Initial state
        print("The application has started!")

    def change_state(self, new_state):
        self.state = new_state

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
    pass
