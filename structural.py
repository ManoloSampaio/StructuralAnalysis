import queue
import networkx as nx
import numpy as np
# Performs the Structural Observability Test.
def SO(A,C):
    A = (np.where(A!=0,1,A))
    C = np.transpose(np.where(C!=0,1,C))
    origin_nodes = sensor_nodes(C)
    if isolated_node_test(A,origin_nodes):
        if rank_test(A,origin_nodes):
            return True
        else:
            return False
    else:
        return False
# Performs the test for isolated node.
def isolated_node_test(A,origin_nodes):
    number_of_state_nodes  = len(A)
    queue_of_nodes = queue.Queue(maxsize=number_of_state_nodes)
    visited_by_origin_node = [0]*number_of_state_nodes
    for node in origin_nodes:
        queue_of_nodes.put(node)
        while queue_of_nodes.empty()==False:
            row=queue_of_nodes.queue[0]
            for i in range(0,len(A[row][:])):
                if A[row][i]==1 and (i in queue_of_nodes.queue)==0 and A[i][i]!=2:
                    queue_of_nodes.put(i)
            A[row][row]=2
            visited_by_origin_node[(queue_of_nodes.get())]=1
        if sum(visited_by_origin_node)==number_of_state_nodes:
            return True
    return False
# Performs the rank test.
def rank_test(A,origin_nodes):
    bipartite_graph = mapping_bipartite(A)
    max_matching,max_matching_size = maximum_matching(bipartite_graph)
    max_matching_list = list(max_matching)
    count = 0
    for edge in max_matching_list:
        if edge[0] in origin_nodes:
            count =count +1
    if count >= len(A)-max_matching_size:
        return True
    else:
        return False
#Performs the maximum_matching test, using a bipartite graph.
def maximum_matching(A_bipartite):
    num_state_nodes = len(A_bipartite)/2
    G =  nx.from_numpy_matrix(np.matrix(A_bipartite))
    max_matching = nx.algorithms.maximal_matching(G)
    max_matching_size = len(max_matching)
    return max_matching,max_matching_size
#Performs the mapping into a bippartite graph.
def mapping_bipartite(A):
    A = A.tolist()
    num_state_nodes = len(A)
    for i in range(0,num_state_nodes):
        save_values = A[i]
        A[i]=[0]*num_state_nodes
        A[i].extend(save_values)
        A.append([0]*2*num_state_nodes)
    return A
#Performs the structural controllability test.
def SC(A,B):
    A = np.transpose(np.where(A!=0,1,A))
    B = np.where(B!=0,1,B)
    origin_nodes = input_nodes(B)
    if isolated_node_test(A,origin_nodes)==True:
        if rank_test(A,origin_nodes):
             return True
        else:
            return False
    else:
        return False
# Get the nodes that recive inputs.
def input_nodes(B):
    origin_nodes = []
    for i in range(0,len(B)):
        if 1 in B[i]:
            origin_nodes.append(i)
    return origin_nodes
# Get the nodes that are connect to the sensor.
def sensor_nodes(C):
    sensor_nodes = []
    for i in range(0,len(C)):
        if 1 in C[i]:
            sensor_nodes.append(i)
    return sensor_nodes
# Get the minimum number of driver nodes.
def MDNS(A):
    A = np.transpose(np.where(A!=0,1,A))
    bipartite_graph = mapping_bipartite(A)
    max_matching,rank = maximum_matching(bipartite_graph)
    print(max_matching)
    number_of_nodes_to_control = len(A)-rank
    max_matching_list = list(max_matching)
    not_matched = []
    matched = []
    for i in range(0,rank):
        not_matched.append(max_matching_list[i][0])
        matched.append(max_matching_list[i][1])
    true_not_matched = actual_not_matched(matched,not_matched,len(A))
    return true_not_matched,number_of_nodes_to_control
# Get the actual not matched nodes of the system.
def actual_not_matched(matched,not_matched,num_of_states):
    matched = [x - num_of_states for x in matched]
    actual_not_matched = []
    for x in not_matched:
        if not (x in matched):
            actual_not_matched.append(x)
    return actual_not_matched
def control_profile(A):
    A = np.transpose(np.where(A!=0,1,A))
    num_of_states = len(A)
    bipartite_graph = mapping_bipartite(A)
    max_matching,rank = maximum_matching(bipartite_graph)
    n_source =0
    n_sink = 0
    n_external_dilation =0
    n_internal_dilation =0
    for edge in max_matching:
        if sum(A[:,edge[0]])==0:
            n_source = n_source+1
        if sum(A[edge[1]-num_of_states,:])==0:
            n_sink = n_sink +1
    n_external_dilation = max(0,n_sink-n_source)
    n_internal_dilation = num_of_states-n_external_dilation-n_source
    return n_source/num_of_states,n_external_dilation/num_of_states,n_internal_dilation/num_of_states
def degree(A):
    A = np.transpose(np.where(A!=0,1,A))
    num_of_states = len(A)
    degree_in = []
    degree_out = []
    for i in range(0,num_of_states):
            degree_in.append(sum(A[i,:]))
            degree_out.append(sum(A[:,i]))
    return degree_in,degree_out