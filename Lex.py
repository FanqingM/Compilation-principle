from Exp2NFA import *
import graphviz

def draw(transitions):
        nfa=Digraph('G',filename='NFAs.gv',format='png')
        for i in range(len(transitions)):
            n1,sym,n2=str(transitions[i][0]),transitions[i][1],str(transitions[i][2])
            nfa.edge(n1,n2,label=sym)
        nfa.view()

bs=1
NFAs=list()
signs=['=','+','×','/','^',',']
begin_states=[bs]

#添加标识符
iden=ExpToNFA(bs)
bs,trans=iden.convert('l(l|d)*')
begin_states.append(bs)
NFAs.extend(trans)

#添加常量
const=ExpToNFA(bs)
bs,trans=const.convert('dd*')
begin_states.append(bs)
NFAs.extend(trans)

for sign in signs:
    s=ExpToNFA(bs)
    bs,trans=s.convert(sign)
    begin_states.append(bs)
    NFAs.extend(trans)

begin_states.pop()
for i in begin_states:
    NFAs.insert(0,(0,'#',i))

draw(NFAs)
