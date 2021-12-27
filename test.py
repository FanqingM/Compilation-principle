import random
from copy import deepcopy
from minimizer import DFA

dfa = DFA()
def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]
state_graph1 = {
    'total_states': [ '1', '2', '3', '4', '5', '6', '7','8','9','10','11','12','13','14','15','16','17','18','19','20' ],
    'initial_states': [ '1' ],
    'termination_states': [ '2', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20' ],
    'state_transition_map': {
        '1': {'2': 'd', '3': ':', '4': '/', '5': '<', '6': 'K', '7': '>', '8': '=', '9': 'l', '10': ',', '11': '×', '12': '+', '13': ';'}, 
        '2': {'14': 'd'}, 
        '3': {'15': '='}, 
        '5': {'16': '>', '17': '='}, 
        '7': {'18': '='}, 
        '9': {'19': 'd', '20': 'l'}, 
        '14': {'14': 'd'}, 
        '19': {'19': 'd', '20': 'l'}, 
        '20': {'19': 'd', '20': 'l'},
    },
    # 'state_transition_map': {'1': {'d': '2', ':': '3', '/': '4', '<': '5', 'K': '6', '>': '7', '=': '8', 'l': '9', ',': '10', '×': '11', '+': '12', ';': '13'}, '2': {'d': '14'}, '3': {'=': '15'}, '5': {'>': '16', '=': '17'}, '7': {'=': '18'}, '9': {'d': '19', 'l': '20'}, '14': {'d': '14'}, '19': {'d': '19', 'l': '20'}, '20': {'d': '19', 'l': '20'}},
    'cins': [ 'd', ':', '/', '<', 'K', '>', '=', 'l', ',', '×', '+', ';' ],  
}
# States: {1, 2, 3, 4, 5, 6, 7}
# Start State: 1
# Final States: {4, 5, 6, 7}
# Transitions: {1: {2: {'b'}, 3: {'a'}}, 2: {4: {'b'}, 3: {'a'}}, 3: {2: {'b'}, 5: {'a'}}, 4: {4: {'b'}, 6: {'a'}}, 5: {7: {'b'}, 5: {'a'}}, 6: {7: {'b'}, 5: {'a'}}, 7: {4: {'b'}, 6: {'a'}}}
# Alphabet: {'b', 'a'}

state_graph5 = {
    'total_states': [ '1', '2','3', '4', '5', '6', '7' ],
    'initial_states': ['1'],
    'termination_states': [ '4', '5', '6', '7' ],
    'state_transition_map': {
        '1': {'2': 'b', '3': 'a'}, '2': {'4': 'b', '3': 'a'}, '3': {'2': 'b', '5': 'a'}, '4': {'4': 'b', '6': 'a'}, '5': {'7': 'b', '5': 'a'}, '6': {'7': 'b', '5': 'a'}, '7': {'4': 'b', '6': 'a'}
    },
    # 'state_transition_map': {'1': {'d': '2', ':': '3', '/': '4', '<': '5', 'K': '6', '>': '7', '=': '8', 'l': '9', ',': '10', '×': '11', '+': '12', ';': '13'}, '2': {'d': '14'}, '3': {'=': '15'}, '5': {'>': '16', '=': '17'}, '7': {'=': '18'}, '9': {'d': '19', 'l': '20'}, '14': {'d': '14'}, '19': {'d': '19', 'l': '20'}, '20': {'d': '19', 'l': '20'}},
    'cins': [ 'b', 'a' ],  
}


state_graph4 = {
    'total_states': [ '1', '2', '3', '4', '5', '6', '7','8','9','10','11','12','13','14','15','16','17','18','19','20' ],
    'initial_states': [ '1' ],
    'termination_states': [ '2', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20' ],
    'state_transition_map': {
        '1': {'2': {'d'}, '3': {':'}, '4': {'/'}, '5': {'<'}, '6': {'K'}, '7': {'>'}, '8': {'='}, '9': {'l'}, '10': {','}, '11': {'×'}, '12': {'+'}, '13': {';'}}, 
        '2': {'14': {'d'}}, 
        '3': {'15': {'='}}, 
        '5': {'16': {'>'}, '17': {'='}}, 
        '7': {'18': {'='}}, 
        '9': {'19': {'d'}, '20': {'l'}}, 
        '14': {'14': {'d'}}, 
        '19': {'19': {'d'}, '20': {'l'}}, 
        '20': {'19': {'d'}, '20': {'l'}},
    },
    'cins': [ 'd', ':', '/', '<', 'K', '>', '=', 'l', ',', '×', '+', ';' ],    
}
 
state_graph2 = {
    'total_states': [ 'A', 'B', 'C', 'D', 'E', 'F', 'S' ],
    'initial_states': [ 'S' ],
    'termination_states': [ 'C', 'D', 'E', 'F' ],
    # 'state_transition_map': {
    #     'S': { 'a': 'A', 'b': 'B' },
    #     'A': { 'a': 'C', 'b': 'B' },
    #     'B': { 'a': 'A', 'b': 'D' },
    #     'C': { 'a': 'C', 'b': 'E' },
    #     'D': { 'a': 'F', 'b': 'D' },
    #     'E': { 'a': 'F', 'b': 'D' },
    #     'F': { 'a': 'C', 'b': 'E' },
    # },
    'state_transition_map': {'S': {'A': 'a', 'B': 'b'}, 'A': {'C': 'a', 'B': 'b'}, 'B': {'A': 'a', 'D': 'b'}, 'C': {'C': 'a', 'E': 'b'}, 'D': {'F': 'a', 'D': 'b'}, 'E': {'F': 'a', 'D': 'b'}, 'F': {'C': 'a', 'E': 'b'}},
    'cins': [ 'a', 'b' ],    
}

state_graph3 = {
    'total_states': { 'A', 'B', 'C', 'D', 'E', 'F', 'S' },
    'initial_states':  'A' ,
    'termination_states': { 'C', 'D', 'E', 'F' },
    'state_transition_map': {
        'S': { 'a': {'A'}, 'b': {'B'} },
        'A': { 'a': {'C'}, 'b': {'B'} },
        'B': { 'a': {'A'}, 'b': {'D'} },
        'C': { 'a': {'C'}, 'b': {'E'} },
        'D': { 'a': {'F'}, 'b': {'D'} },
        'E': { 'a': {'F'}, 'b': {'D'} },
        'F': { 'a': {'C'}, 'b': {'E'} },
    },
    #  'state_transition_map': {
    #     'S': { 'a': 'A', 'b': 'B' },
    #     'A': { 'a': 'C', 'b': 'B' },
    #     'B': { 'a': 'A', 'b': 'D' },
    #     'C': { 'a': 'C', 'b': 'E' },
    #     'D': { 'a': 'F', 'b': 'D' },
    #     'E': { 'a': 'F', 'b': 'D' },
    #     'F': { 'a': 'C', 'b': 'E' },
    # },
    'cins': { 'a', 'b' },    
}
 
 
 
def hopcroft_algorithm( G ):
    cins                   = set( G['cins'] )
    termination_states     = set( G['termination_states'] ) 
    total_states           = set( G['total_states'] )
    state_transition_map   = G['state_transition_map']
    not_termination_states = total_states - termination_states

 
    def get_source_set( target_set, char ):
        source_set = set()
        for state in total_states:
            try:
                if state_transition_map[state][char] in target_set:
                    source_set.update( state )
            except KeyError:
                pass
        return source_set
 
    P = [ termination_states, not_termination_states ]
    W = [ termination_states, not_termination_states ]
 
    while W:
        
        A = random.choice( W )
        W.remove( A )
 
        for char in cins:
            X = get_source_set( A, char )
            P_temp = []
            
            for Y in P:
                S  = X & Y
                S1 = Y - X
                
                if len( S ) and len( S1 ):
                    P_temp.append( S )
                    P_temp.append( S1 )
                    
                    if Y in W:
                        W.remove( Y )    
                        W.append( S )
                        W.append( S1 )
                    else:
                        if len( S ) <= len( S1 ):
                            W.append( S )
                        else:
                            W.append( S1 )
                else:
                    P_temp.append( Y )
            P = deepcopy( P_temp )
    return P

def minimize(G):
    def get_source_set2( target_set, char ):
        source_set = set()
        for state in total_states:
            try:
                if state_transition_map[state][char] in target_set:
                    source_set.update( state )
            except KeyError:
                pass
        return source_set
    cins                   = set( G['cins'] )
    termination_states     = set( G['termination_states'] ) 
    total_states           = set( G['total_states'] )
    state_transition_map   = G['state_transition_map']
    # print(state_transition_map)
    not_termination_states = total_states - termination_states
    

    ## 调整顺序 没有实际作用，仅仅为了下面的根据最小划分生成最小化DFA,对于graph1不需要 对于graph2要
    # for key in state_transition_map:
    #     state_transition_map[key] = dict(zip(state_transition_map[key].values(), state_transition_map[key].keys()))

    # print(G['state_transition_map'])

    for key in state_transition_map:
        G['state_transition_map'][key] = dict(zip(G['state_transition_map'][key].values(), G['state_transition_map'][key].keys()))
    
    # print(G['state_transition_map'])
    dfa.alphabet = cins
    min_states = hopcroft_algorithm(G)
    print(min_states)
    # 获取最小划分
    new_total_states = []
    new_final_states = []
    new_start_state = 'c'
    new_transition = set()
    x = dict()
    # print("min_states",min_states)



    for key in state_transition_map:
        state_transition_map[key] = dict(zip(state_transition_map[key].values(), state_transition_map[key].keys()))


    for state_set in min_states:
        min_state = min(state_set)
        if(len((termination_states)&(state_set)) != 0):
            ## 说明这个min_state是终态
            new_final_states.append(min_state)
        if(set(G['initial_states']).issubset(state_set)):
            new_start_state = min_state
        # print(min_state)
        # print(type(min_state))
        new_total_states.append(min_state)
        for state in state_set:
            if(state_transition_map.__contains__(state)):
                # print(state)
                # print(state_transition_map[state])
                for c in cins:
                    
                    temp = get_key(state_transition_map[state],c)
                    # print(temp)
                    ## 这里由于是DFA，对于一个输入字符，只有唯一的可能状态，所以temp长度只能为0/1
                    if(len(temp)!= 0):
                        # print(temp[0],c)
                        for state_set2 in min_states:
                            if(temp[0] in state_set2):
                                # print(state_set2,temp[0],c)
                                ##就添加由min_state到min（state_set2)的连接,中间是c
                                # print(min_state,c,min(state_set2))
                                dfa.add_transition(min_state,c,min(state_set2))
                            
    dfa.states = new_total_states   
    dfa.start_state = new_start_state
    dfa.final_states = set(new_final_states)             
    dfa.print()
    dfa.draw()
    ## 初态是别人走不到 终态是不能走到别人


    # for 

    # print(dfa.transitions['C'].keys())


minimize(state_graph5)


