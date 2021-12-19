from Automata import Automata, nfa_convert_to_dfa
from minimizer import DFA

def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]
nfa=Automata()
dfa1 = DFA()

# Add NFA States
for i in range(0,8):
    nfa.add_state(i)

# Set Initial and Final(s) State
nfa.add_final_state(7)
nfa.add_start_state([0])

# Register Alphabet
nfa.add_symbol('a')
nfa.add_symbol('b')

# Register Transitions
nfa.add_transition(0,Automata.epsilon(),5)
nfa.add_transition(6,Automata.epsilon(),7)
nfa.add_transition(5,'a',5)
nfa.add_transition(5,'b',5)
nfa.add_transition(5,Automata.epsilon(),1)
nfa.add_transition(1,'a',3)
nfa.add_transition(1,'b',4)
nfa.add_transition(3,'a',2)
nfa.add_transition(4,'b',2)
nfa.add_transition(2,Automata.epsilon(),6)
nfa.add_transition(6,'a',6)
nfa.add_transition(6,'b',6)


dfa=nfa_convert_to_dfa(nfa)

dfa.print()

dfa1.states = dfa.states
dfa1.start_state = dfa.start_states
dfa1.final_states = dfa.final_states
dfa1.transitions = dfa.transitions
dfa1.alphabet = dfa.alphabet

print(type(dfa1))
# dfa1.print()
# dfa1 = dfa

# dfa1.print()
# dfa.draw('x.png')

# Minimize
dfa1.minimize()

# Print and Draw After Diagram
print('=' * 10, 'After Minimization', '=' * 10)
dfa1.print()

