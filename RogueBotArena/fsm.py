class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}

    def add_transition(self, input, next_state):
        self.transitions[input] = next_state

    def get_next_state(self, input):
        return self.transitions.get(input, None)

class FSM:
    def __init__(self, initial_state):
        self.current_state = initial_state

    def update(self, input):
        next_state = self.current_state.get_next_state(input)
        if next_state:
            self.current_state = next_state
        return self.current_state.name
        