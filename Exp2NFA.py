import networkx as nx
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
    def __init__(self):
        self.states=set() #状态集合
        self.start_states=1 #起始状态
        self.state_num=1 #总状态数
        self.final_states=set() #终止状态集合 
        self.transitions=[] #状态转移集
        self.alphabet=set() #可接受的字符集
        self.current_state=self.start_states #当前的状态数
        self.state_loss=0 #需要剪掉的状态数
        self.nodes=[] #标识符转化成的node
        self.Nodes=Node()
        self.top=0 #栈顶指针

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
            if(squence[i]<='z' and squence[i]>='a'):
                symbol.append(squence[i])
                squence.pop(i)
                if(i<len(squence) and squence[i]<='z' and squence[i]>='a' ):
                    connection.append('-')
                    squence.pop(i)
                elif (i<len(squence) and squence[i]=='('):
                    connection.append('-')
            
               
            else:
                connection.append(squence[i])
                if(i+1<len(squence) and (squence[i]=='*' or squence[i]==')') 
                            and squence[i+1]<='z' and squence[i+1]>='a'):
                    connection.append('-')   
                squence.pop(i)              
        return symbol,connection

    #给所有标识符初始化起始状态和终止状态
    def init_node(self,symbol):
        for i in symbol:
            current_state=self.current_state
            node=self.Nodes.make_node(current_state,i,current_state+1)
            self.nodes.append(node)
            self.current_state+=2


    #处理a|b
    def handle_unite(self,a,b):
    
        if(a.symbol>='a' and a.symbol<='z'):
            self.transitions.append((a.begin_state,a.symbol,a.end_state))
        if(b.symbol>='a' and b.symbol<='z'):
            self.transitions.append((b.begin_state,b.symbol,b.end_state))

        current_state=self.current_state
        self.transitions.append((current_state,'#',a.begin_state))
        self.transitions.append((current_state,'#',b.begin_state))
        self.transitions.append((a.end_state,'#',current_state+1))
        self.transitions.append((b.end_state,'#',current_state+1))
        self.current_state+=2

        node=self.Nodes.make_node(current_state,'|',current_state+1)
        self.nodes.pop(self.top+1)
        self.nodes.pop(self.top)
        self.nodes.insert(self.top,node)
   
    #处理ab
    def handle_join(self,a,b):

      
        if(a.symbol=='|' or a.symbol=='+' or b.symbol=='|' or b.symbol=='+'):#左右至少一个节点集
            if(a.symbol>='a' and a.symbol<='z'):
                self.transitions.append((a.begin_state,a.symbol,a.end_state))
                self.transitions.append((a.end_state,'#',b.begin_state))
            if(b.symbol>='a' and b.symbol<='z'):
                b.begin_state=a.end_state
                b.end_state-=1
                self.transitions.append((b.begin_state,b.symbol,b.end_state))
            else:
                 self.transitions.append((a.end_state,'#',b.begin_state))
                
        else:#左右都不是节点集
            b.begin_state=a.end_state 
            b.end_state-=1
            self.transitions.append((a.begin_state,a.symbol,a.end_state))
            self.transitions.append((b.begin_state,b.symbol,b.end_state))
         
        

       
        
        node=self.Nodes.make_node(a.begin_state,'+',b.end_state)
        self.nodes.pop(self.top+1)
        self.nodes.pop(self.top)
        self.nodes.insert(self.top,node)
        self.state_loss+=1

    #处理a*
    def handle_closure(self,a):
        current_state=self.current_state
        a.begin_state-=self.state_loss
        a.end_state-=self.state_loss
        if(a.symbol>='a' and a.symbol<='z'):
            self.transitions.append((a.begin_state,a.symbol,a.end_state))

        self.transitions.append((current_state,'#',current_state+1))
        self.transitions.append((a.end_state,'#',a.begin_state))
        self.transitions.append((current_state,'#',a.begin_state))
        self.transitions.append((a.end_state,'#',current_state+1))
        self.current_state+=2

        node=self.Nodes.make_node(current_state,'|',current_state+1)
        self.nodes.pop(self.top)
        self.nodes.insert(self.top,node)



    def convert(self,exp):
        model=ExpToNFA()
        squence=model.read_regular_expression(exp)
        symbol,connection=model.classify(squence)
        model.init_node(symbol)
        i=0
        while(len(model.nodes)>1 or len(connection)!=0):
            if(connection[i]=='|'):
                if (i+1<len(connection) and connection[i+1]=='('):
                    model.top+=1
                    connection.pop(i+1)
                    i+=1
                else:
                    model.handle_unite(model.nodes[model.top],model.nodes[model.top+1])
                    connection.pop(i)
            elif(connection[i]=='-'):
                if (i+1<len(connection) and connection[i+1]=='('):
                    model.top+=1
                    connection.pop(i+1)
                    i+=1
                else:
                    model.handle_join(model.nodes[model.top],model.nodes[model.top+1])
                    connection.pop(i)
            elif(connection[i]=='*'):
                model.handle_closure(model.nodes[model.top])
                connection.pop(i)
            elif(connection[i]==')'):
                model.top-=1
                connection.pop(i)
                i-=1       
        model.Print()
        nfa=Digraph('G',filename='NFA.gv',format='png')
        for i in range(len(model.transitions)):
            n1,sym,n2=str(model.transitions[i][0]),model.transitions[i][1],str(model.transitions[i][2])
            nfa.edge(n1,n2,label=sym)
        nfa.view()
            
    
    def Print(self):
        print(self.transitions)

#test              
entity=ExpToNFA()
entity.convert('a*b(c|d)e')
# entity.convert('l(l|d)*')

    