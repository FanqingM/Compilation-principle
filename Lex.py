from Exp2NFA import *
import graphviz

def draw(transitions,end_states):
        nfa=Digraph('G',filename='NFAs.gv',format='png')
        for i in range(len(transitions)):
            if(transitions[i][2] in end_states):
                s='doublecircle'
            else:
                s='circle'
            if(transitions[i][0]==0):
                c='green'
            else:
                c='grey'
            n1,sym,n2=str(transitions[i][0]),transitions[i][1],str(transitions[i][2])
            nfa.node(name=n1,label=n1,color=c,shape='circle')
            nfa.node(name=n2,label=n2,color='grey',shape=s)
            nfa.edge(n1,n2,label=sym)
        nfa.view()
    
def NFA():
    bs=1
    NFAs=list()
    signs=['=','+','×','/','^',',']
    begin_states=[bs]
    end_states=[]

    #添加标识符
    iden=ExpToNFA(bs)
    bs,trans,ends=iden.convert('l(l|d)*')
    begin_states.append(bs)
    NFAs.extend(trans)
    end_states.extend(ends)

    #添加常量
    const=ExpToNFA(bs)
    bs,trans,ends=const.convert('dd*')
    begin_states.append(bs)
    NFAs.extend(trans)
    end_states.extend(ends)


    for sign in signs:
        s=ExpToNFA(bs)
        bs,trans,ends=s.convert(sign)
        begin_states.append(bs)
        NFAs.extend(trans)
        end_states.extend(ends)
        
    begin_states.pop()
    for i in begin_states:
        NFAs.insert(0,(0,'#',i))

    draw(NFAs,end_states)
    return trans,end_states
