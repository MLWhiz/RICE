'''program
'''
from collections import deque

def bfs_visited(ugraph, start_node):
    '''Functio to visit bfs'''
    visited = set() 
    visited.add(start_node)
    queue = deque()
    queue.append(start_node)
    while len(queue)!=0:
        inspectnode = queue.popleft()
        for newnode in ugraph[inspectnode]:
            if newnode not in visited:
                visited.add(newnode)
                queue.append(newnode)
    return visited


def cc_visited(ugraph):
    '''Functio to visit bfs'''
    concomp= [] 
    remainingnodes = [vertex for vertex in ugraph.iterkeys()]
    while len(remainingnodes)!=0:
        arbit_node = remainingnodes[0]
        set_of_nodes = bfs_visited(ugraph, arbit_node)
        concomp.append(set_of_nodes)
        for elem in set_of_nodes:
            remainingnodes.remove(elem)

    return concomp

def largest_cc_size(ugraph):
    '''Functio to visit bfs'''
    concomp = cc_visited(ugraph)
    max_cc = 0
    for elem in concomp:
        if len(elem)>max_cc:
            max_cc = len(elem)
    return max_cc

def compute_resilience(ugraph, attack_order):
    '''Functio to visit bfs'''
    return_list = []
    return_list.append(largest_cc_size(ugraph))
    for node in attack_order:
        ugraph.pop(node, None)
        for _, value in ugraph.iteritems():
            if node in value:
                value.remove(node)
        return_list.append(largest_cc_size(ugraph))
    return return_list
    