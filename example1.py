from minimizer import DFA

def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]

dfa = DFA()

# Add DFA States
dfa.add_state(1)
dfa.add_state(2)
dfa.add_state(3)
dfa.add_state(4)
dfa.add_state(5)

# Set Initial and Final(s) State
dfa.add_start_state(1)
dfa.add_final_state(1)
dfa.add_final_state(5)

# Register Alphabet
dfa.add_symbol('a')
dfa.add_symbol('b')

# Register Transitions
dfa.add_transition(1, 'a', 3)
dfa.add_transition(1, 'b', 2)
dfa.add_transition(2, 'b', 1)
dfa.add_transition(2, 'a', 4)
dfa.add_transition(3, 'b', 4)
dfa.add_transition(3, 'a', 5)
dfa.add_transition(4, 'a', 4)
dfa.add_transition(4, 'b', 4)
dfa.add_transition(5, 'a', 3)
dfa.add_transition(5, 'b', 2)

b = "bbaa"
# s = {b[0]}
# print(get_key(dfa.transitions[1],s)[0])
# print(dfa.start_state)

# dfa.DFACode(b)
# Print and Draw Before Diagram
print('=' * 10, 'Before Minimization', '=' * 10)
dfa.print()
dfa.draw()

# Minimize
dfa.minimize()

# Print and Draw After Diagram
print('=' * 10, 'After Minimization', '=' * 10)
dfa.print()

dfa.DFACode(b)
# dfa.draw("dfa_after")