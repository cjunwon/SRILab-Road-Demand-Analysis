import pickle
import numpy as np
import networkx as nx
import pandas as pd
import time
from collections import defaultdict

# Import B_matrix and node_coordinates
with open(r'graph_centrality_codes/nodes_edges_weighted.pickle', 'rb') as handle:
    B_matrix_weighted, node_coordinates_weighted = pickle.load(handle)

# Import distance array 
'''
Distance array format:

1st col - distance (m)
2nd col - time (s)
3rd col - time in traffic (s)

'''
with open(r'graph_centrality_codes/distance.pickle', 'rb') as handle:
    distance_array = pickle.load(handle)  

# Import Origin_Destination_Node_Added (from 02_block_node_pairing.py)
Origin_Destination_Node_Added = pd.read_pickle('intermediate_files/Origin_Destination_Node_Added.pkl')


# Display network
Hillside_edgelist = B_matrix_weighted[:,0:2].astype(int)
NetworkEdgeWt_pre = distance_array[:,2]
# NetworkEdgeWt_pre[NetworkEdgeWt_pre == 0] = 1

temp = np.expand_dims(NetworkEdgeWt_pre, axis = 1)

FinalEdge = np.concatenate((Hillside_edgelist, temp), axis = 1).astype(int)
FinalEdge_df = pd.DataFrame(FinalEdge, columns = ['from', 'to', 'weight'])

G = nx.from_pandas_edgelist(FinalEdge_df, source = 'from', target = 'to', edge_attr = True)

Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
G0 = G.subgraph(Gcc[0])

print('Connected components: ' + str(len(Gcc)))
print('Node count in largest component: ' + str(len(G0.nodes())))
nx.draw(G,pos=node_coordinates_weighted[:,0:2],node_size=2)


# Check number of unique nodes identified into blocks
unique_nodes = np.unique(Origin_Destination_Node_Added['w_node_id'])
print('Total Nodes: ' + str(len(Origin_Destination_Node_Added['w_node_id'])))
print('Total Unique Nodes: ' + str(len(unique_nodes)))

# Subset Origin_Destination_Node_Added
origin_destination_ids_df = Origin_Destination_Node_Added[['w_node_id', 'h_node_id', 'S000_adjusted', 'SA01_adjusted', 'SA02_adjusted', 'SA03_adjusted', 'SE01_adjusted', 'SE02_adjusted', 'SE03_adjusted', 'SI01_adjusted', 'SI02_adjusted', 'SI03_adjusted']]

# Create dictionary of origin nodes and destination nodes
origin_destination_ids_dict = defaultdict(list)
for origin, destination, S000_adjusted, SA01_adjusted, SA02_adjusted, SA03_adjusted, SE01_adjusted, SE02_adjusted, SE03_adjusted, SI01_adjusted, SI02_adjusted, SI03_adjusted in zip(origin_destination_ids_df['w_node_id'], origin_destination_ids_df['h_node_id'], origin_destination_ids_df['S000_adjusted'], origin_destination_ids_df['SA01_adjusted'], origin_destination_ids_df['SA02_adjusted'], origin_destination_ids_df['SA03_adjusted'], origin_destination_ids_df['SE01_adjusted'], origin_destination_ids_df['SE02_adjusted'], origin_destination_ids_df['SE03_adjusted'], origin_destination_ids_df['SI01_adjusted'], origin_destination_ids_df['SI02_adjusted'], origin_destination_ids_df['SI03_adjusted']):
    origin_destination_ids_dict[origin].append((destination, S000_adjusted, SA01_adjusted, SA02_adjusted, SA03_adjusted, SE01_adjusted, SE02_adjusted, SE03_adjusted, SI01_adjusted, SI02_adjusted, SI03_adjusted))


# Create empty dataframe to store origin ID, destination ID, and path
origin_destination_path_df = pd.DataFrame(columns = ['origin_id', 'destination_id', 'path', 'S000_adjusted', 'SA01_adjusted', 'SA02_adjusted', 'SA03_adjusted', 'SE01_adjusted', 'SE02_adjusted', 'SE03_adjusted', 'SI01_adjusted', 'SI02_adjusted', 'SI03_adjusted'])
origin_destination_path_list=[]

# Keep track of nodes that have no connection
no_connection_df = pd.DataFrame(columns = ['origin_id', 'destination_id', 'S000_adjusted', 'SA01_adjusted', 'SA02_adjusted', 'SA03_adjusted', 'SE01_adjusted', 'SE02_adjusted', 'SE03_adjusted', 'SI01_adjusted', 'SI02_adjusted', 'SI03_adjusted'])
no_connection_list=[]

# Main loop to find shortest path between each origin and destination
start=time.time()

counter=1
# for node_id in unique_nodes[:42]:
for node_id in unique_nodes:
    
    print(counter)
    try:
        path_dict = nx.single_source_dijkstra_path(G, node_id, cutoff=None, weight='weight')
    except nx.NetworkXNoPath:
        continue

    for destination_with_adj in origin_destination_ids_dict[node_id]:
        if destination_with_adj[0] in path_dict:
            # print(1)
            # startdf=time.time()
            # origin_destination_path_df.loc[len(origin_destination_path_df.index)] = [node_id, destination_with_adj[0], path_dict[destination_with_adj[0]], destination_with_adj[1], destination_with_adj[2], destination_with_adj[3], destination_with_adj[4], destination_with_adj[5], destination_with_adj[6], destination_with_adj[7], destination_with_adj[8], destination_with_adj[9], destination_with_adj[10]]
            origin_destination_path_list.append([node_id, destination_with_adj[0], path_dict[destination_with_adj[0]], destination_with_adj[1], destination_with_adj[2], destination_with_adj[3], destination_with_adj[4], destination_with_adj[5], destination_with_adj[6], destination_with_adj[7], destination_with_adj[8], destination_with_adj[9], destination_with_adj[10]])
            # enddf=time.time()
            # print(str(enddf-startdf))
        else:
            # no_connection_df.loc[len(no_connection_df.index)] = [node_id, destination, destination_with_adj[1], destination_with_adj[2], destination_with_adj[3], destination_with_adj[4], destination_with_adj[5], destination_with_adj[6], destination_with_adj[7], destination_with_adj[8], destination_with_adj[9], destination_with_adj[10]]
            no_connection_list.append([node_id, destination, destination_with_adj[1], destination_with_adj[2], destination_with_adj[3], destination_with_adj[4], destination_with_adj[5], destination_with_adj[6], destination_with_adj[7], destination_with_adj[8], destination_with_adj[9], destination_with_adj[10]])
    counter+=1
end=time.time()

print('Time taken to find paths: ' + str(end-start))

origin_destination_path_df=pd.DataFrame(origin_destination_path_list)
no_connection_df=pd.DataFrame(no_connection_list)

print('Total node pairs parsed: ' + str(len(origin_destination_path_df) + len(no_connection_df)))
print('Total node pairs connected: ' + str(len(origin_destination_path_df)))
print('Total node pairs not connected: ' + str(len(no_connection_df)))

origin_destination_path_df.to_pickle('origin_destination_path_df.pkl')

# Export results to pickle
with open(r'intermediate_files/Shortest_Path_Results.pickle', 'wb') as handle:
    pickle.dump([origin_destination_path_list,no_connection_list,origin_destination_path_df,no_connection_df], handle, protocol=pickle.HIGHEST_PROTOCOL)

# with open(r"script_output.pickle","rb") as handle:
#     origin_destination_path_list,no_connection_list,origin_destination_path_df,no_connection_df=pickle.load(handle)