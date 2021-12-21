import networkx as nx
from networkx.classes.function import to_undirected
import numpy as np
from graphviz import Digraph
from networkx.algorithms.shortest_paths.weighted import single_source_bellman_ford
from networkx.classes import digraph

class Node(object):
    class node(object):
        def __init__(self,begin_state,symbol,end_state):
            self.begin_state=begin_state
            self.end_state=end_state
            self.symbol=symbol
            
    def make_node(self,b_s,sym,e_s):
        return self.node(b_s,sym,e_s)

class ExpToNFA:
    def __init__(self,start):
        self.states=set() #状态集合
        self.start_states=start #起始状态
        self.state_num=1 #总状态数
        self.final_states=set() #终止状态集合 
        self.transitions=[] #状态转移集
        self.alphabet=set() #可接受的字符集
        self.current_state=self.start_states #当前的状态数
        self.state_loss=0 #需要剪掉的状态数
        self.nodes=[] #标识符转化成的node
        self.Nodes=Node()
        self.top=-1 #栈顶指针
        self.connection=['(',')','|','*','-']


    def add_state(self,state):
        self.states.add(state)
    
    def add_final_state(self,state):
        if isinstance(state,int):
            self.final_states.add(state)
        else:
            self.final_states=self.final_states|state

    
    def read_regular_expression(self,expression):
        alphabet=[]
        for i in expression:
            #标识符加入，不重复
            if(i!='|' and i!='(' and i!=')' and i!='*'):
                if(i not in self.alphabet):
                    self.alphabet.add(i)
            alphabet.append(i)
        return alphabet 
    
    #分出起始符和连接符
    def classify(self,squence):
       
        squence=list(squence)
        symbol=[]
        connection=[]
       
        while(len(squence)>0):
            i=0
            # if(squence[i]<='z' and squence[i]>='a'):
            if(squence[i] not in self.connection):
                symbol.append(squence[i])
                if(i+1<len(squence) and squence[i+1] not in self.connection):
                    connection.append('-')
                elif (i+1<len(squence) and squence[i+1]=='('):
                    connection.append('-')
                squence.pop(i)
            
               
            else:
                connection.append(squence[i])
                if(i+1<len(squence) and (squence[i]=='*' or squence[i]==')') 
                            and squence[i+1] not in self.connection):
                    connection.append('-')   
                squence.pop(i)              
        return symbol,connection

    #获取节点中缀表达式
    def getInfix(self,squence):
        i=0
        infix=list()
        while(len(squence)>0):
             if(squence[i] not in self.connection):
                 infix.append(squence[i])
                 if(i+1<len(squence) and squence[i+1] not in self.connection ):
                    infix.append('-')
                 elif (i+1<len(squence) and squence[i+1]=='('):
                    infix.append('-')
                 squence.pop(i)
                 
             else:
                infix.append(squence[i])
                if(i+1<len(squence) and (squence[i]=='*' or squence[i]==')') 
                            and squence[i+1]<='z' and squence[i+1]>='a'):
                    infix.append('-')   
                squence.pop(i)      
        
        for x in range(len(infix)):
            if(infix[x] not in self.connection):    
                infix[x]=self.nodes[i]
                i+=1
                
        return infix

    #中缀转后缀
    def infixToPostfix(self,infixexpr):
        priority={"(":1,'-':3,'|':2,'*':4}
        opStack = list()
        postfixList = []
        tokenList = list(infixexpr)
        for token in tokenList:
            if token!='(' and token!=')' and token!='*' and token !='|' and token !='-':
                postfixList.append(token)
            elif token == '(':
                opStack.append(token)
            elif token == ')':
                topToken = opStack.pop()
                while topToken != '(':
                    postfixList.append(topToken)
                    topToken = opStack.pop()
            else:
                while len(opStack)>0 and \
                (priority[opStack[len(opStack)-1]] >= priority[token]):
                    postfixList.append(opStack.pop())
                opStack.append(token)

        while len(opStack)>0:
            postfixList.append(opStack.pop())
        return postfixList

    #给所有标识符初始化起始状态和终止状态
    def init_node(self,symbol):
        for i in symbol:
            current_state=self.current_state
            node=self.Nodes.make_node(current_state,i,current_state+1)
            self.transitions.append((current_state,i,current_state+1))
            self.nodes.append(node)
            self.current_state+=2


    #处理a|b
    def handle_unite(self,a,b):
    
        if(a.symbol not in self.connection):
            self.transitions.append((a.begin_state,a.symbol,a.end_state))
        if(b.symbol not in self.connection):
            self.transitions.append((b.begin_state,b.symbol,b.end_state))

        current_state=self.current_state
        self.transitions.append((current_state,'#',a.begin_state))
        self.transitions.append((current_state,'#',b.begin_state))
        self.transitions.append((a.end_state,'#',current_state+1))
        self.transitions.append((b.end_state,'#',current_state+1))
        self.current_state+=2

        node=self.Nodes.make_node(current_state,'|',current_state+1)
        self.nodes.append(node)
   
    #处理ab
    def handle_join(self,a,b):
        if(a.symbol=='|' or a.symbol=='+' or b.symbol=='|' or b.symbol=='+'):#左右至少一个节点集
            if(a.symbol not in self.connection):
                self.transitions.append((a.begin_state,a.symbol,a.end_state))
                self.transitions.append((a.end_state,'#',b.begin_state))
            if(b.symbol not in self.connection):
                self.transitions.append((b.begin_state,b.symbol,b.end_state))
                self.transitions.append((a.end_state,'#',b.begin_state))
            else:
                 self.transitions.append((a.end_state,'#',b.begin_state))
                
        else:#左右都不是节点集
            self.transitions.append((a.begin_state,a.symbol,a.end_state))
            self.transitions.append((b.begin_state,b.symbol,b.end_state))
            self.transitions.append((a.end_state,'#',b.begin_state))
         
        node=self.Nodes.make_node(a.begin_state,'+',b.end_state)
        self.nodes.append(node)
        # self.state_loss+=1

    #处理a*
    def handle_closure(self,a):
        current_state=self.current_state
        # a.begin_state-=self.state_loss
        # a.end_state-=self.state_loss
        if(a.symbol not in self.connection):
            self.transitions.append((a.begin_state,a.symbol,a.end_state))

        self.transitions.append((current_state,'#',current_state+1))
        self.transitions.append((a.end_state,'#',a.begin_state))
        self.transitions.append((current_state,'#',a.begin_state))
        self.transitions.append((a.end_state,'#',current_state+1))
        self.current_state+=2

        node=self.Nodes.make_node(current_state,'#',current_state+1)
        self.nodes.append(node)
    
    def print_matrix(self):
        trans=[]
        alphabet=list(self.alphabet)
        alphabet.append('#')
        for i in range(self.current_state):
            for j in range(len(alphabet)):
                trans.append('-')
        trans=np.array(trans)
        trans=trans.reshape(self.current_state,len(alphabet))
        for edge in self.transitions:
            trans[int(edge[0])][alphabet.index(str(edge[1]))]=edge[2]
        print("   ",end='')
        for state in alphabet:
            print(state,end=' ')
        print('')
        for i in range(trans.shape[0]):
            print('{:<3d}'.format(i),end='')
            for j in range(trans.shape[1]):
                print('%s' % trans[i][j],end=' ')
            print('')


    def check_start(self):
        states=list()
        start_state=list()
        for i in range(len(self.transitions)):
            states.append(0)
        for i in self.transitions:
            states[i[2]-self.start_states]=1
        for i in range(len(states)):
            if(states[i]==0):
                start_state.append(i+1)
        return start_state[0]+self.start_states

    def check_end(self):
        states=list()
        end_state=list()
        for i in range(self.current_state):
            states.append(0)
        for i in self.transitions:
            states[i[0]-self.start_states]=1
        for i in range(len(states)):
            if(states[i]==0):
                end_state.append(i+1)
        self.add_final_state(end_state[0]+self.start_states-1)
        return end_state[0]+self.start_states
                

    def convert(self,exp):
        
        model=ExpToNFA(self.start_states)
        squence=model.read_regular_expression(exp)
        symbol,connection=model.classify(squence)
        model.init_node(symbol)
        infix=model.getInfix(squence)
        postfix=model.infixToPostfix(infix)
        model.nodes=[]
        for i in range(len(postfix)):
            if(postfix[i] not in connection):
                model.nodes.append(postfix[i])
            else:
                if(postfix[i]=='|'):
                    node2=model.nodes.pop()
                    node1=model.nodes.pop()
                    model.handle_unite(node1,node2)
                elif(postfix[i]=='-'):
                    node2=model.nodes.pop()
                    node1=model.nodes.pop()
                    model.handle_join(node1,node2)
                else:
                    node=model.nodes.pop()
                    model.handle_closure(node)
       
        # model.start_states=0
        # model.transitions.append((model.start_states,'#',model.check_start()))
        model.transitions=set(model.transitions)
        model.transitions=list(model.transitions)
        model.Print()
        # nfa=Digraph('G',filename='NFA.gv',format='png')
        # for i in range(len(model.transitions)):
        #     n1,sym,n2=str(model.transitions[i][0]),model.transitions[i][1],str(model.transitions[i][2])
        #     nfa.edge(n1,n2,label=sym)
        # nfa.view()
        # model.print_matrix()
        model.check_end()
        return model.current_state,model.transitions,model.final_states
            
    
    def Print(self):
        print(self.transitions)

#test              
# entity=ExpToNFA(1)
# entity.convert('a*b(c|d)e')
# entity.convert('(a|b)*cba')
# entity.convert('l(l|d)*')
# entity.convert('dd*')

 