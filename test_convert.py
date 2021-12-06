from Automata import Automata, nfa_convert_to_dfa

nfa=Automata()

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
dfa.draw('x.png')

