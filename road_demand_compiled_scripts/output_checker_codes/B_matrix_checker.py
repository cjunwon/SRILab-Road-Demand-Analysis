import pickle
import pandas as pd
import numpy as np

with open(r'../graph_centrality_codes/nodes_edges_weighted.pickle', 'rb') as handle:
    B_matrix_weighted, node_coordinates_weighted = pickle.load(handle)
    
with open(r'../graph_centrality_codes/distance.pickle', 'rb') as handle:
    distance_array = pickle.load(handle)  
    
#distance_array (1st col - distance (m), 2nd col - time (s), 3rd col - time in traffic (s))

# Initialize array of 0s with 10 columns and add to B_matrix_weighted
zero_columns = np.zeros((B_matrix_weighted.shape[0], 10))
B_matrix_weighted_array = np.hstack((B_matrix_weighted, zero_columns))
B_matrix_weighted_array = B_matrix_weighted_array.astype(float)

print('Shape of original B_matrix_weighted: ' + str(B_matrix_weighted.shape))
print('Shape of new B_matrix_weighted_array (before dict conversion): ' + str(B_matrix_weighted_array.shape))

B_matrix_weighted_dict = {(row[0], row[1]): row for row in B_matrix_weighted_array}

print('Shape of new B_matrix_weighted_dict: ' + str(len(B_matrix_weighted_dict)))



# Create a new array that only contains the first two elements of each row
first_two_columns = B_matrix_weighted[:, :2]

# Find duplicate rows in the new array
unique_rows, counts = np.unique(first_two_columns, axis=0, return_counts=True)

print('Number of unique node pairs: ' + str(len(unique_rows)))
