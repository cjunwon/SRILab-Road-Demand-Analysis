import pickle
import networkx as nx
import pandas as pd
import numpy as np
import time

with open(r'graph_centrality_codes/nodes_edges_weighted.pickle', 'rb') as handle:
    B_matrix_weighted, node_coordinates_weighted = pickle.load(handle)
    
with open(r'graph_centrality_codes/distance.pickle', 'rb') as handle:
    distance_array = pickle.load(handle)  
    
#distance_array (1st col - distance (m), 2nd col - time (s), 3rd col - time in traffic (s))


origin_destination_path_df = pd.read_pickle('origin_destination_path_df.pkl')



# Initialize array of 0s and add as a column to B_matrix_weighted

zero_column = np.zeros((B_matrix_weighted.shape[0], 1))
B_matrix_weighted_array = np.hstack((B_matrix_weighted, zero_column))
B_matrix_weighted_array = B_matrix_weighted_array.astype(int)

print(B_matrix_weighted_array.shape)

B_matrix_weighted_df = pd.DataFrame(B_matrix_weighted_array)


# Approach 1: Indexing the original B_matrix_weighted in array form (Issue: In theory this should be faster, and if you print individual values commented, it should be correct but it doesn't update the original array for some reason)


start=time.time()

for index, row in origin_destination_path_df.iterrows():
    path = row['path']
    for i in range(len(path) - 1):
        # Find the indices of the path elements in the B array
        idx1 = np.where(B_matrix_weighted_array[:, 0] == path[i])[0]
        idx2 = np.where(B_matrix_weighted_array[:, 1] == path[i+1])[0]
        
        if len(idx1) > 0 and len(idx2) > 0:
            idx = np.intersect1d(idx1, idx2)
            # print(idx)
            if len(idx) > 0:
                B_matrix_weighted_array[idx, 6] = B_matrix_weighted_array[idx, 6] + row['S000_adjusted']
                # print(row['S000_adjusted'])

end=time.time()

print(end-start)
print('Number of node pairs updated in B_matrix_weighted (approach 1): ' + str(len(B_matrix_weighted_array[B_matrix_weighted_array[:, 6] != 0])))


# Approach 2: Indexing the original B_matrix_weighted in dataframe form (This would be slower than the first approach but is working)

# This iterates over each row of the origin_destination_path_df dataframe and for each row, it iterates over each pair of adjacent nodes in the path column.
# For each pair of nodes, it checks if the nodes are present in the first and second columns (or reversed) of the B_matrix_weighted_df dataframe.
# If the nodes are present, it adds the S000_adjusted value to the 6th column of the B_matrix_weighted_df dataframe.

start=time.time()

for index, row in origin_destination_path_df.iterrows():
    for i in range(len(row['path']) - 1):
        if (row['path'][i] in B_matrix_weighted_df[0] and row['path'][i + 1] in B_matrix_weighted_df[1]):
            B_matrix_weighted_df.loc[(B_matrix_weighted_df[0] == row['path'][i]) & (B_matrix_weighted_df[1] == row['path'][i + 1]), 6] += row['S000_adjusted']
        elif (row['path'][i] in B_matrix_weighted_df[1] and row['path'][i + 1] in B_matrix_weighted_df[0]):
            B_matrix_weighted_df.loc[(B_matrix_weighted_df[1] == row['path'][i]) & (B_matrix_weighted_df[0] == row['path'][i + 1]), 6] += row['S000_adjusted']

end=time.time()

print(end-start)
print('Number of node pairs updated in B_matrix_weighted (approach 2): ' + str(len(B_matrix_weighted_df[B_matrix_weighted_df[6] != 0])))


# Convert B_matrix_weighted_df back to a numpy array

B_matrix_weighted_updated = B_matrix_weighted_df.to_numpy()

# Export B_matrix_weighted_updated as a pickle file

with open('B_matrix_weighted_updated.pickle', 'wb') as handle:
    pickle.dump(B_matrix_weighted_updated, handle, protocol=pickle.HIGHEST_PROTOCOL)