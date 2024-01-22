import pickle
import pandas as pd
import numpy as np
import time

# Import B_matrix and node_coordinates
with open(r'graph_centrality_codes/nodes_edges_weighted.pickle', 'rb') as handle:
    B_matrix_weighted, node_coordinates_weighted = pickle.load(handle)

with open(r"intermediate_files/Shortest_Path_Results.pkl","rb") as handle:
    origin_destination_path_list,no_connection_list,origin_destination_path_df,no_connection_df=pickle.load(handle)

'''
origin_destination_path_df column index reference:

0: origin_id
1: destination_id
2: path
3: S000_adjusted
4: SA01_adjusted
5: SA02_adjusted
6: SA03_adjusted
7: SE01_adjusted
8: SE02_adjusted
9: SE03_adjusted
10: SI01_adjusted
11: SI02_adjusted
12: SI03_adjusted

'''

print('Number of rows in df: ' + str(len(origin_destination_path_list)))

# Make a copy of the origin_destination_path_list and origin_destination_path_df
origin_destination_path_list_copy = origin_destination_path_list.copy()
origin_destination_path_df_copy = origin_destination_path_df.copy()

# For quick testing with subsets you can uncomment the following 2 lines:
# origin_destination_path_list_copy = origin_destination_path_list[0:100]
# origin_destination_path_df_copy = origin_destination_path_df[0:100]


# Rename columns
origin_destination_path_df_copy.columns = ['origin_id', 'destination_id', 'path', 'S000_adjusted', 'SA01_adjusted', 'SA02_adjusted', 'SA03_adjusted', 'SE01_adjusted', 'SE02_adjusted', 'SE03_adjusted', 'SI01_adjusted', 'SI02_adjusted', 'SI03_adjusted']

# Find all unique paths in origin_destination_path_df_copy's path column
pairlist_actual=[]

for j in range(len(origin_destination_path_list_copy)):
    path = origin_destination_path_list_copy[j][2]
    for i in range(len(path) - 1):
        pair=(min([path[i],path[i+1]]),max([path[i],path[i+1]]))
        if pair not in pairlist_actual:
            pairlist_actual.append(pair)

print('Number of pairs & updates we should get in the end: ' + str(len(pairlist_actual)))

# --------------------------------------------------------------------

# Initialize array of 0s with 10 columns and add to B_matrix_weighted
zero_columns = np.zeros((B_matrix_weighted.shape[0], 10))
B_matrix_weighted_array = np.hstack((B_matrix_weighted, zero_columns))
B_matrix_weighted_array = B_matrix_weighted_array.astype(float)

print('Dimensions of B_matrix_weighted_array: ', B_matrix_weighted_array.shape)

print('Number of rows in origin_destination_path_df', len(origin_destination_path_df))


# Converting B_matrix_weighted to a dictionary for faster lookups (O(1) lookups, faster)
B_matrix_weighted_dict = {(row[0], row[1]): row for row in B_matrix_weighted_array}

start = time.time()

for _, row in origin_destination_path_df_copy.iterrows():
    path = row['path']
    for i in range(len(path) - 1):
        pair = (path[i], path[i+1])
        reverse_pair = (path[i+1], path[i])

        if pair in B_matrix_weighted_dict:
            B_matrix_weighted_dict[pair][6:16] += row['S000_adjusted':'SI03_adjusted']
        elif reverse_pair in B_matrix_weighted_dict:
            B_matrix_weighted_dict[reverse_pair][6:16] += row['S000_adjusted':'SI03_adjusted']

# Convert the dictionary back to a numpy array
B_matrix_weighted_array = np.array(list(B_matrix_weighted_dict.values()))

end = time.time()

print(end - start)

print('Number of updates from Approach 2: ' + str(sum(B_matrix_weighted_array[:, 6] != 0)))

if sum(B_matrix_weighted_array[:, 6] != 0) == len(pairlist_actual):
    print('Approach 2 update count matches expected update count.')

# Export B_matrix_weighted_aray as a pickle file

with open(r'intermediate_files/B_matrix_weighted_updated.pickle', 'wb') as handle:
    pickle.dump(B_matrix_weighted_array, handle, protocol=pickle.HIGHEST_PROTOCOL)