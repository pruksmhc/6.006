# Note that infinity can be represented by float('inf') in Python.

################################################################################
# You do not need to implement anything in this section below.
import operator
import math

#from collections import Counter 

def dist(loc1, loc2):
    xdiff = loc1[0] - loc2[0]
    ydiff = loc1[1] - loc2[1]
    return math.sqrt(xdiff * xdiff + ydiff * ydiff)

import heapq
import itertools
# Borrowed heavily from https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.entry_finder = {}
        self.REMOVED = '<removed>'
        self.counter = itertools.count()
        self.num_elements = 0
        self.num_actions = 0

    def add(self, item, priority):
        if item in self.entry_finder:
            self.remove(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.heap, entry)
        self.num_actions += 1
        self.num_elements += 1

    def remove(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED
        self.num_elements -= 1

    def pop(self):
        self.num_actions += 1
        while self.heap:
            priority, count, item = heapq.heappop(self.heap)
            if item is not self.REMOVED:
                self.num_elements -= 1
                del self.entry_finder[item]
                return item, priority
        raise KeyError('Pop from an empty priority queue')

    def head(self):
        priority, count, item = self.heap[0]
        return item, priority

    def empty(self):
        return self.num_elements == 0

# You do not need to implement anything in this section above.
################################################################################

# TODO: Implement both parts (a) and (b) with this function. If target is None,
# then return a list of tuples as described in part (a). If target is not None,
# then return a path as a list of states as described in part (b).
def dijkstra(n, edges, source, target=None):  
    v_d={}
    v_p ={}
   # #print('WOAH"')
    q = PriorityQueue()
    for v in edges: 
        if v == source:
            q.add(v,0 )
            v_d[v] = 0

        else:
            q.add(v, float("inf"))
            v_d[v] = float("inf")

    while q.num_elements > 0:
        u = q.pop()
        if u[0] == source:
            v_d[u[0]] = 0 
            v_p[u[0]] = None
        else:
            v_d[u[0]] = u[1] #currnet minimum 
 
        if u[0] == target:
            #see I wnat to get into those top colleges.  Because i wnat to have power.k
            path = [] 
            path.append(target)
            min_d = v_d[u[0]]
            n = target
            try:
                while v_p[n] is not None:
                    n = v_p[n]
                    path.append(n)
            except KeyError as e:
                pass
           # #print(path)
            path.reverse()
            ##print((path, min_d))
            #print(path)
            print("num_actions is")
            print(q.num_actions)
            return (path, min_d)


        for e in edges[u[0]]:
            if u[1] + e[1] < v_d[e[0]] :
                v_d[e[0]] = u[1] + e[1] 
                v_p[e[0]] = u[0]
                q.add(e[0], u[1] + e[1] )
                #now zip them togehter. 

    sorted_v_d = sorted(v_d.items(), key=operator.itemgetter(1))
    final  =[]
    print("num_actions is")
    print(q.num_actions)

    for i in sorted_v_d:
        #print(i[0])
        if i[0] in v_p:
            entry = (i[0], i[1], v_p[i[0]])
            final.append(entry)
       # #print(final)

    return final

    #initialize the graph. 



# TODO: Implement part (c).
def bidirectional(n, edges, source, target):
    q_f = PriorityQueue()
    q_b = PriorityQueue()
    u_f_d = {} 
    u_b_d={} 
    min_d = float('inf')
    p_f= {}
    p_b={}
    edges_b={}



    for v in edges.keys(): 
        for e in edges[v]: 
            if e[0] not in edges_b : #if no  v1 = e[0] 
                 edges_b[e[0]] = [] #intiialize 
                 edges_b[e[0]].append(((v, e[1]))) # set of edges. 
            else:
                edges_b[e[0]].append((v, e[1])) #get the edges 

        if v == source:
            q_f.add(v,0 )
            u_f_d[v] = 0
            u_b_d[v] = float('inf')
        elif v == target:
            q_b.add(v,0 )
            u_b_d[v] = 0
            u_f_d[v] = float('inf')
        else:
            q_f.add(v, float("inf"))
            q_b.add(v, float("inf"))
            u_b_d[v] = float('inf')
            u_f_d[v] = float("inf")



    while q_f.empty() is False and q_b.empty() is False :
        u_f , priority_f= q_f.head()
        u_b, priority_b = q_b.head()
        if priority_f< priority_b:
            u_f = q_f.pop()
            if u_f[0] in p_b: 
                if u_f_d[u_f[0]] + u_b_d[u_f[0]] < min_d:  #compare to (s,t) path
                    intersect = u_f[0]
                    min_d = u_f_d[u_f[0]] + u_b_d[u_f[0]]  #update the global minimum 
            if u_f[0]  == source: 
                u_f_d[u_f[0]] = 0 
                p_f[u_f[0]]= None
            for e in edges[u_f[0]]:
                if priority_f + e[1] < u_f_d[e[0]]:
                    u_f_d[e[0]] = priority_f + e[1]
                    p_f[e[0]] = u_f[0]
                    q_f.add(e[0], priority_f + e[1] )
        else:
            u_b = q_b.pop()
            ##print(u_b)
            if u_b[0] in p_f: 

                if u_f_d[u_b[0]] + u_b_d[u_b[0]] < min_d: 
                    intersect = u_b[0]
                    min_d = u_f_d[u_b[0]] + u_b_d[u_b[0]]  #update the global minimum 

            if u_b[0] == target:
                u_b_d[u_b[0]] = 0 
                p_b[u_b[0]] = None
            for e in edges_b[u_b[0]]:
               if priority_b+ e[1] < u_b_d[e[0]]:
                    u_b_d[e[0]]= u_b_d[u_b[0]] + e[1]
                    p_b[e[0]] = u_b[0]
                    q_b.add(e[0], priority_b + e[1] )

        n_f, priority_f = q_f.head()
        n_b, priority_b = q_b.head()

        if priority_f + priority_b > min_d:
            path = [] 
            path.append(intersect)
            v = intersect
            try:
                while p_f[v] is not None:
                    v = p_f[v] 
                    path.append(v)
            except KeyError as e:
                pass
            path.reverse()
            path2 = [] 
            v = intersect
            try:
                while p_b[v] is not None:
                    v= p_b[v]
                    path2.append(v)
            except KeyError as e:
                pass
            path = path +path2 
            #print(path)
            print("num_actions is")
            print(q_f.num_actions + q_b.num_actions)
            return (path, u_f_d[intersect]+ u_b_d[intersect])

# TODO: Implement part (d).
def astar(locs, edges, source, target): 
   
    v_d={}
    v_p ={}
    q = PriorityQueue()
    for v in edges: 
        if v == source:
            q.add(v,0 )
            v_d[v] = 0
        else:
            q.add(v, float("inf"))
            v_d[v] = float("inf")

    while q.num_elements > 0:
        u = q.pop()

        if u[0] == source:
            v_d[u[0]] = 0 
            v_p[u[0]] = None
        else:
            v_d[u[0]] = u[1] #currnet minimum 
        if u[0] == target:
            path = [] 
            path.append(target)
            min_d = v_d[u[0]]
            n = target
            try:
                while v_p[n] is not None:
                    n = v_p[n]
                    path.append(n)
            except KeyError as e:
                pass
            path.reverse()
            #print(path)
            print("num_actions is")
            print(q.num_actions)
            return (path, min_d)
        for e in edges[u[0]]:
            if u[1] + dist(locs[u[0]], locs[e]) < v_d[e] :
                v_d[e] = u[1] + dist(locs[u[0]], locs[e])
                v_p[e]= u[0]
                q.add(e, u[1] + dist(locs[u[0]], locs[e]) )
    sorted_v_d = sorted(v_d.items(), key=operator.itemgetter(1))
    final  =[]
    for i in sorted_v_d:
        if i[0] in v_p:
            entry = (i[0], i[1], v_p[i[0]])
            final.append(entry)
    print("num_actions is")
    print(q.num_actions)
    return final








    #n list of lcoatiosn, dictionary of edges mapping node ut o a list of nodes v (no weights), sourece node s, target node t. 
