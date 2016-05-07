################################################################################
#
# States are represented by 3-tuples of integers in the range 0, ..., k.
#
# Transitions are 2-tuples of states (start_state, end_state), where start_state
# is the start of the transition and end_state is the end of the transition.
#
# Reachable states should be represented by a 3-tuple (state, length, previous)
# where state is the reachable state, length is the length of the path to get
# there, and previous is the previous state. For the 0 length path to the start,
# that would be (start, 0, start).
#
################################################################################

# start is a state, a 3-tuple (x, y, z) where 0 <= x, y, z <= k
# transitions is a list of 2-tuples of 3-tuples (x, y, z)
#   where 0 <= x, y, z <= k.
# Note that the start state is reachable through a path of length 0.

#((0,10, 20), (9, 19, 20)) 



def reachable_states(start, transitions):
    # TODO: Implement part a. 
    #storing into a hashmap. 
   # #print("here'")
    list_t = {}
    q= [] #pop from the back. 
    result= []
    visited={}
    c_state= {}
    #seen =[]
    #building an adjacency list.
    for t in transitions: 
    	#storing into hashmap. 
        visited[t[0]] = None
        visited[t[1]] = None
        #print("inserting"+str(t[0]))
    	if t[0] not in list_t: 
    		list_t[t[0]] = [] 
    		list_t[t[0]].append(t[1])
    	else:
            list_t[t[0]].append(t[1])


    q.append(start) 
    c_state[start] = (0, start)
    visited[start] = True
    while len(q) > 0:
        cur = q.pop(len(q)-1)
        res = (cur, c_state[cur][0], c_state[cur][1])
    	result.append(res)
    	if cur in list_t: #if reachable 
	        for n in list_t[cur]:
                    if visited[n] is None:
                        q.insert(0, n)
                        visited[n] = True
                        c_state[n] = (c_state[cur][0]+1, cur)

#c_state has the information about the parent nodes. 
    return result


#can i make it so that 
				

def reachable_states_machine(start, transitions):
    # TODO: Implement part a. 
    #storing into a hashmap. 
   # #print("here'")
    list_t = {}
    q = [] #pop from the back. 
    result= []
    visited={}
    c_state= {}
    #seen =[]
    #building an adjacency list.
    for t in transitions: 
        #storing into hashmap. 
        visited[t[0]] = None
        visited[t[1]] = None
        #print("inserting"+str(t[0]))
        if t[0] not in list_t: 
            list_t[t[0]] = [] 
            list_t[t[0]].append(t[1])
        else:
            list_t[t[0]].append(t[1])


    q.append(start) 
    c_state[start] = (0, start)
    visited[start] = True
    while len(q) > 0:
        cur = q.pop(len(q)-1)
        res = (cur, c_state[cur][0], c_state[cur][1])
        result.append(res)
        if cur in list_t: #if reachable 
            for n in list_t[cur]:
                    if visited[n] is None:
                        q.insert(0, n)
                        visited[n] = True
                        c_state[n] = (c_state[cur][0]+1, cur)

#c_state has the information about the parent nodes. 
    return result, c_state
# Returns either a path as a list of reachable states if the target is
# reachable or False if the target isn't reachable.
def simple_machine(k, start, target):
    # TODO: Implement part b.
    #target is reach

    #calculate ((a,b,c),(a+1,b+1,c+1)), one transition.  
    transitions = []
    for a in range(0,k+1,1): 
        for b in range(0,k+1,1):
            for c in range(0, k+1): 
                #a+1, b+1, c+1
                if a <= k-1 and b <= k-1 and c <= k-1: 
                    transitions.append(((a,b,c), (a+1, b+1, c+1)))
                if a> 0 and b > 0 and c>0: 
                    transitions.append(((a,b,c), (a-1,b-1,c-1)))
                if a > 0 : 
                    transitions.append(((a,b,c), (a-1, b,c)))
                if a <= k-1: 
                    transitions.append(((a,b,c), (a+1, b,c)))
   # #print(transitions)
    ##print("trans'")
    res, c_state= reachable_states_machine(start, transitions) 
    ##print(res)

    for item in res: 
        if target == item[0]:
            path=[]
            path.append(target)   
            key =target 
            while key != start: 
                key = c_state[key]
                #print("KEY")
                #print(key)
                key = key[1] #find the predecessor
                path.append(key)
                ##print(key)
            path.reverse()
            ##print(path)
            return path 

    ##print("return flase")
    return False


# Returns either False if the mutual exclusion property is satisfied or
# a minimum-length counterexample as a list of reachable states.

def mutual_exclusion_1():
    transitions = []
    for a in range(0, 4,1): 
        for b in range(0,4,1):
            for c in range(1, 3, 1): 
                #a+1, b+1, c+1
                if a is 0:
                    #(0,b,c) -> (1,b,1)
                    transitions.append(((a,b,c),(a+1, b, 1)))
                if b is 0: 
                    #(a,0,c) ->(a,1,2)
                    transitions.append(((a,b,c),(a, b+1, 2)))
                if a is 1 and b is 0: 
                    #(1,0,c) -> (3,0,c)
                    transitions.append(((a,b,c),(3, b, c)))
                if a is 0 and b is 1:  
                    # (0,1,c) -> (0,3,c)
                    transitions.append(((a,b,c),(0, 3, c)))
                if a is 1 and b <3 and c is 2: #1,b, 2 -> 3,b,2
                    transitions.append(((a,b,c),(3, b, c)))
                if a <3 and b is 1 and c is 1:  #a,1, 1 -> a,3,1
                    transitions.append(((a,b,c),(a, 3, c)))
                if a is 3: # 3, b, c- >  0,b,c
                    transitions.append(((a,b,c),(0, b, c)))
                if b is 3:  #a,3,c -> a,0,c
                    transitions.append(((a,b,c),(a, 0, c)))
    #print(transitions)
    res = reachable_states((0,0,1), transitions) 
    #print(res)
    for item in res: 
        if item[0] == (3,3,1) or item[0] == (3,3,2):
            if (3,3,1) in res: 
                key = (3,3,1)
            else: 
                key= (3,3,2)
            #print("Found")
            table = {}
            #finding shortest path

            path=[]
            for item in res:
                table[item[0]] = item 
            #print(table) 
            path.append(key)
            while key != (0,0,1): 
                key = table[key]
                key = key[2] #find the predecessor
                path.append(key)
                #print(key)
            path.reverse()
            #print(path)
            return path 
    else: 
        return False


 

# Returns either False if the mutual exclusion property is satisfied or
# a minimum-length counterexample as a list of reachable states.
def mutual_exclusion_2():
    # TODO: Implement part d.
        transitions = []
        for a in range(0, 4,1): 
            for b in range(0,4,1):
                for c in range(0, 3, 1): 
                #a+1, b+1, c+1
                    #print("inserting")
                   # #print((a,b,c))
                    if a is 0 and c is 0: 
                        transitions.append(((a,b,c), (1,b,0)))
                    if b is 0 and c is 0: 
                        transitions.append(((a,b,c), (a,1,0)))
                    if a is 1 : 
                        transitions.append(((a,b,c), (2,b,1)))
                    if b is 1 : 
                        transitions.append(((a,b,c), (a,2,2)))
                    if a is 2  and c != 1: 
                        transitions.append(((a,b,c), (0,b,c)))
                    if b is 2 and c != 2: 
                        transitions.append(((a,b,c), (a,0,c)))
                    if b is 2 and c is 2: 
                        transitions.append(((a,b,c), (a, 3,c)))
                    if a is 2 and c is 1: 
                        transitions.append(((a,b,c), (3,b,c)))
                    if a is 3: 
                        transitions.append(((a,b,c), (0,b,0)))
                    if b is 3: 
                        transitions.append(((a,b,c), (a,0,0)))

        #print(transitions)
        #print("TRANSITIONS")
        res = reachable_states((0,0,0), transitions) 
        #print(res)
        for item in res: 
            if item[0] == (3,3,1) or item[0] == (3,3,2) or item[0] ==(3,3,0):
                #print("FOUND FOUND")
                if (3,3,1) in res: 
                    key = (3,3,1)
                else: 
                    key= (3,3,2)
                #print("Found")
                table = {}
                #finding shortest path

                path=[]
                for item in res:
                    table[item[0]] = item 
                #print(table) 
                path.append(key)
                while key != (0,0,0): 
                    key = table[key]
                    key = key[2] #find the predecessor
                    path.append(key)
                    #print(key)
                path.reverse()
                #print(path)
                return path 
        else: 
            return False









