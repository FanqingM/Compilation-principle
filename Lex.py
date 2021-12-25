from Exp2NFA import *
from Automata import *
from minimizer import *
import graphviz



def Draw(transitions,end_states,f_n):
        nfa=Digraph('G',filename=f_n,format='png')
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
    keyword=['PROGRAM','BEGIN','END','CONST','VAR','WHILE','DO','IF','THEN']
    signs=['+','×','/',':=','=','<>','>','>=','<','<=',';',',']
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

    #关键词
    const=ExpToNFA(bs)
    bs,trans,ends=const.convert('K')
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

    Draw(NFAs,end_states,'NFAs.gv')
    return NFAs,end_states

def formDFA(trans):
    nfa=generateNFA(trans)
    dfa=nfa_convert_to_dfa(nfa)
    dfa.draw('DAFs.gv')
    dfa.print()

    return dfa

def Minimize(dfa):
    dfa1=DFA()
    dfa1.states = dfa.states
    dfa1.start_state = dfa.start_states
    dfa1.final_states = dfa.final_states
    dfa1.transitions = dfa.transitions
    dfa1.alphabet = dfa.alphabet
    dfa1.minimize()

def readProgram(program):
    signs=['+','-','*','/',':=','=','<>','>','>=','<','<=','(',')','；',',']
    words=[]
    current_word=''
    for i in range(len(program)):
        if(i+1<len(program) and program[i+1]!=' ' and program[i] not in signs and program[i]!=' '):
            current_word+=program[i]

        elif(program[i] in signs):
            words.append(current_word)
            current_word=''
            #二元符
            if( i+1<len(program) and program[i+1] in signs):
                 words.append(program[i]+program[i+1])
                 i+=2
            #一元符
            else:
                 words.append(program[i])
                 i+=1

        elif( i+1<len(program) and program[i+1] in signs):
             words.append(current_word)
             current_word=''

        else:
            if(current_word!=''):
                current_word+=program[i]
                words.append(current_word)
                current_word=''

    return words

def output(words,DFA):
    keyword=['PROGRAM','BEGIN','END','CONST','VAR','WHILE','DO','IF','THEN']
    signs=['+','-','*','/',':=','=','<>','>','>=','<','<=','(',')','；',',']
    for word in words:
        if(word in keyword):
            input='K'
            DFA.DFAcode(word)
        elif(word in signs):
            input='S'
            DFA.DFAcode(word)


    
words=readProgram("VAR i1,i2,i3")

nfa,ends=NFA()
dfa=formDFA(nfa)
mini=Minimize(dfa)
