import networkx as nx
from graphviz import Source

def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]

class DFA:

    def __init__(self):
        self.states = set()    ## 状态集合
        self.start_state = 0   ## 起始状态集合
        self.final_states = set()  ## 终止状态集合
        self.transitions = {}      ## 状态转移矩阵
        self.alphabet = set()      ## 可接受的字符

    def add_state(self, state):
        self.states.add(state)

    def add_start_state(self, state):
        self.start_state = state

    def add_final_state(self, state):
        self.final_states.add(state)

    def add_symbol(self, symbol):
        self.alphabet.add(symbol)

    def add_transition(self, f_state, symbol, t_state):
        if f_state not in self.transitions:
            self.transitions.update({f_state: {}})

        if t_state not in self.transitions[f_state]:
            self.transitions[f_state].update({t_state: set()})

        self.transitions[f_state][t_state].add(symbol)

    def print(self):
        print("States:", self.states)
        print("Start State:", self.start_state)
        print("Final States:", self.final_states)
        print("Transitions:", self.transitions)
        print("Alphabet:", self.alphabet)


## 这是画图函数，环境原因没有实验
    def draw(self, filename=None):
        G = nx.DiGraph()

        for i in self.states:
            s = 'doublecircle' if i in self.final_states else 'circle'
            f = 'grey' if i == self.start_state else 'white'
            G.add_node(i, shape=s, fillcolor=f, style='filled')

        for i, d in self.transitions.items():
            for k, v in d.items():
                l = ','.join(v)
                G.add_edge(i, k, label=l)

        plot = Source(nx.drawing.nx_agraph.to_agraph(G))

        if not filename:
            return plot
        # plot.show()
        plot.render(filename, format='png')    
        
    ## 这个函数是用来找到最小划分的
    def hopcroft(self):
        P = [ self.final_states, self.states.difference(self.final_states) ]
        ## P一开始是起始态和终止态的划分，最后经过迭代变成最终的划分
        W = [ self.final_states ]

        while len(W) > 0:
            A = W.pop()  ## 注意这东西pop出来的是一个set
            
            for c in self.alphabet:
                X = set()
                for f_state, t_state in self.transitions.items():
                    ## f是起始状态，t是接受字母，以及接受字母后跳转到的状态，一个f可能有多个t
                    for k, s in t_state.items():
                        if c in s and k in A:
                            X.update(set([f_state]))
                            ## update方法是合并集合
                            ## 如果存在一个字母表中的字符使得这个状态接受这个字符后跳到终态，那么将这个状态合并进X
                            ## X是接受一个字符可以到终态的集合

                for Y in P:
                    if X.intersection(Y) != set() and Y.difference(X) != set():
                        ## 当现在的分解的list中存在一个set，以及字母表中的一个元素，使得这个set经过这个元素
                        ## 后，跳转到的状态的集合不全在分解的集合的子集中，就把Y分解，重新加入结果集
                        P.append(X.intersection(Y))
                        P.append(Y.difference(X))
                        P.remove(Y)

                        ## 之后我们还需要更新W
                        if Y in W:
                            W.append(X.intersection(Y))
                            W.append(Y.difference(X))
                            W.remove(Y)
                        else:
                            if len(X.intersection(Y)) <= len(Y.difference(X)):
                                W.append(X.intersection(Y))
                            else:
                                W.append(Y.difference(X))
        # print('hopcroft', P)
        ## 通过这个算法，可以产出最小化划分
        return P

    def minimize(self):
        min_states = self.hopcroft()

        for state_set in min_states:
            ## state_set是一个set
            if len(state_set) > 1:
                min_state = min(state_set)
                ## 以set中最小的作为化简后的DFA的新的状态
                for state in state_set:
                    ## state是一个数
                    self.transitions[min_state].update(self.transitions[state])
                    ## 更新化简后的DFA的新的状态的状态转移矩阵中的一条记录
                    ## transitions是个三元组
                    if state != min_state:
                        self.transitions.pop(state)
                        self.states.discard(state)

                changes = []
                for s, _ in self.transitions.items():
                    for t, _ in self.transitions[s].items():
                        if t in state_set and t != min_state:
                            changes.append((t, s))
                            ## 我们之前将新状态用原来状态的组合中的最小的代替，所以状态转移中需要添加上，没有被
                            ## 代替的状态到其他状态的跳转
                
                for t, s in changes:
                    self.transitions[s][min_state] = self.transitions[s].pop(t)

                if self.start_state in state_set:
                    self.start_state = min_state
                
                changes = []
                for fs in self.final_states:
                    if fs in state_set:
                        changes.append(fs)

                for s in changes:
                    self.final_states.discard(fs)
    
    ## DFA代码化
    def DFACode(self,variables):
        res = ""
        for i in range(len(variables)):
            if variables[i] not in self.alphabet:
                print("error")
                break
            if i == 0:
                s = {variables[i]}
                # temp是初态接受这个字母到达的状态的集合，是list
                temp = get_key(self.transitions[self.start_state],s)
                if len(temp) == 0:
                    print("error")
                    break
                else:
                    t_tmp = temp[0]
                    # print(t_tmp)
            else:
                s = {variables[i]}
                # print(s)
                # print(t_tmp)
                # temp是初态接受这个字母到达的状态的集合，是list
                temp = get_key(self.transitions[t_tmp],s)
                if len(temp) == 0:
                    print("error")
                    break
                else:
                    t_tmp = temp[0]
                    # if(t_tmp in self.final_states):
                    #     res+=variables[i]
                    # print(t_tmp)
        if t_tmp in self.final_states:
            res = "<" + "V," + variables + ">"
            print(res)
            
                
