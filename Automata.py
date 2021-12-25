import networkx as nx
from graphviz import Source
from graphviz import Digraph


class Automata:
    def __init__(self,alphabet=set()):
        self.states = set()  ## 状态集合
        self.start_states = None  ## 起始状态集合
        self.final_states = set()  ## 终止状态集合
        self.transitions = dict()  ## 状态转移矩阵
        self.alphabet = alphabet  ## 可接受的字符

    @staticmethod
    def epsilon():
        return ":e:"

    def add_state(self, state):
        self.states.add(state)

    def add_start_state(self, state):
        self.start_states = state

    def add_final_state(self, state):
        if isinstance(state,int):
            self.final_states.add(state)
        else:
            self.final_states=self.final_states|state

    def add_symbol(self, symbol):
        self.alphabet.add(symbol)

    def add_transition(self, f_state, symbol, t_state):
        if f_state not in self.transitions:
            self.transitions.update({f_state: {}})

        if t_state not in self.transitions[f_state]:
            self.transitions[f_state].update({t_state: set()})

        self.transitions[f_state][t_state].add(symbol)

    def get_e_closure(self,state)->set:
        allstates=set()

        while len(state)!=0:
            s=state.pop()
            allstates.add(s)
            if s in self.transitions:
                for temp in self.transitions[s].items():
                    if self.epsilon() in temp[1]:
                        allstates.add(temp[0])
                        allstates=(allstates|self.get_e_closure([temp[0]]))
        return allstates

    def get_transition(self,f_state,symbol)->set:
        transitions=set()
        if f_state in self.transitions:
            for t_state in self.transitions[f_state]:
                if symbol in self.transitions[f_state][t_state]:
                    transitions.add(t_state)
        return transitions

    def get_transition_set(self,f_states:set,symbol)->set:
        transitions=set()
        for state in f_states:
            transitions=transitions|(self.get_transition(state,symbol))
        return transitions



    def print(self):
        print("States:", self.states)
        print("Start State:", self.start_states)
        print("Final States:", self.final_states)
        print("Transitions:", self.transitions)
        print("Alphabet:", self.alphabet)

    def draw(self, filename=None):
        # 实例化一个Digraph对象(有向图)，name:生成的图片的图片名，format:生成的图片格式
        G = Digraph(name=filename, comment="test", format="png")
        for i in self.states:
            if i in self.final_states:
                s = 'doublecircle'
            else:
                s = 'circle'
            if i == self.start_states:
                f = 'green'
            else:
                f = 'gray'
            # s = 'doublecircle' if i in self.final_states else 'circle'
            # f = 'grey' if i == self.start_state else 'green'
            G.node(name = str(i),label = str(i),color = f,shape = s)
            # G.add_node(i, shape=s, fillcolor=f, style='filled')


        for i, d in self.transitions.items():
            for k, v in d.items():
                l = ','.join(v)
                G.edge(str(i), str(k), label=l)
        #print(G.source)
        
        # 画图，filename:图片的名称，若无filename，则使用Digraph对象的name，默认会有gv后缀
        # directory:图片保存的路径，默认是在当前路径下保存
        G.view(filename=filename)
        
        # 跟view一样的用法(render跟view选择一个即可)，一般用render生成图片，不使用view=True,view=True用在调试的时候
        #G.render(filename='NFATODFA',view=True)


def generateNFA(res: list):
    nfa=Automata()

    in_nodes = set()
    out_nodes = set()

    for t in res:
        out_nodes.add(t[0])
        in_nodes.add(t[2])

        if t[1] == '#':
            nfa.add_symbol(Automata.epsilon()) # 添加终结符
            nfa.add_transition(t[0],Automata.epsilon(),t[2])
        else:
            nfa.add_symbol(t[1])
            nfa.add_transition(t[0],t[1],t[2])

    finals=in_nodes.difference(out_nodes)
    nfa.add_final_state(finals) # 添加终态

    nfa.add_start_state([0]) # 添加初态

    all_nodes=in_nodes|out_nodes
    for node in all_nodes:
        nfa.add_state(node) # 添加状态节点

    return nfa


## 子集法将nfa转为dfa
def nfa_convert_to_dfa(nfa:Automata)->Automata:
    e_closure=[]
    start_states=nfa.get_e_closure(nfa.start_states)
    e_closure.append(list(start_states))
    count=1

    dfa=Automata(nfa.alphabet-set(nfa.epsilon()))
    dfa.add_state(count)
    dfa.add_start_state(count)

    index=0
    while index<count:
        cur_state=e_closure[index]
        inter=set(cur_state)&nfa.final_states
        if  len(inter)!=0:
            dfa.add_final_state(index+1)
        for vt in dfa.alphabet:
            to_state=nfa.get_transition_set(cur_state,vt)
            to_state=nfa.get_e_closure(to_state)

            if to_state :
                if to_state not in e_closure:
                    e_closure.append(to_state)
                    count+=1
                    dfa.add_state(count)
                dfa.add_transition(index+1,vt,e_closure.index(to_state)+1)
        index+=1
    dfa.add_final_state(count)
    return dfa
 
        


if __name__ == "__main__":
    res = [(7, '#', 5), (9, '#', 7), (9, '#', 10), (4, '#', 8), (2, '#', 9), (5, 'd', 6), (1, 'l', 2), (7, '#', 3),
           (3, 'l', 4), (6, '#', 8), (8, '#', 7), (8, '#', 10)]

    nfa = generateNFA(res)
    dfa = nfa_convert_to_dfa(nfa)

    dfa.print()
