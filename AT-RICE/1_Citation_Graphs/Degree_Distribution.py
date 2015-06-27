'''Create a Digraph and compute indegree and in_degree_distribution'''

EX_GRAPH0 = {0:set([1,2]),1:set([]),2:set([])}
EX_GRAPH1 = {0:set([1,4,5]),1:set([2,6]) , 2:set([3]),3:set([0]),4:set([1]),5:set([2]),6:set([])}
EX_GRAPH2 = {0:set([1,4,5]), 1:set([2,6]), 2:set([3,7]), 3:set([7]),4:set([1]),5:set([2]),6:set([]),7:set([3]),8:set([1,2]),9:set([0,3,4,5,6,7])}


def make_complete_graph(num_nodes):
    '''make complete graph'''
    graph_dict={}
    for index in range(0,num_nodes):
        graph_dict[index]=set([x for x in range(0,num_nodes) if x!=index])
    return graph_dict



def compute_in_degrees(digraph):
    '''compute in degree'''
    degree_dict={}
    edges=[]
    for key in digraph.iterkeys():
        for node in digraph[key]:
            edges.append([key,node])
        degree_dict[key]=0
    for edge in edges:
        if edge[1] in degree_dict:
            degree_dict[edge[1]]+=1
        else:
            degree_dict[edge[1]]=1
    return degree_dict
    


def in_degree_distribution(digraph):
    '''in degree dist'''
    indegrees = compute_in_degrees(digraph)
    deg_dist_dict={}
    for _,value in indegrees.iteritems():
        if value in deg_dist_dict:
            deg_dist_dict[value]+=1
        else:
            deg_dist_dict[value]=1
    return deg_dist_dict



