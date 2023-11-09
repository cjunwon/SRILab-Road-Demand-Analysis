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

with open(r"script_output.pickle","rb") as handle:
    origin_destination_path_list,no_connection_list,origin_destination_path_df,no_connection_df=pickle.load(handle)

# origin_destination_path_df columns:
# ----------------------------------
# 0: origin_id
# 1: destination_id
# 2: path
# 3: S000_adjusted
# 4: SA01_adjusted
# 5: SA02_adjusted
# 6: SA03_adjusted
# 7: SE01_adjusted
# 8: SE02_adjusted
# 9: SE03_adjusted
# 10: SI01_adjusted
# 11: SI02_adjusted
# 12: SI03_adjusted

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

print(B_matrix_weighted_array.shape)

print(len(origin_destination_path_df))

# --------------------------------------------------------------------
# Approach 2 is significantly faster than Approach 1, and both produce the same results.
# Uncomment the code for Approach 1 (vice versa) to test the other approach.
# --------------------------------------------------------------------

# Approach 1: Indexing the original B_matrix_weighted in array form (Linear, very slow)

# start=time.time()
# pairlist_test_1=[]

# for index, row in origin_destination_path_df_copy.iterrows():
#     path = row['path']
#     for i in range(len(path) - 1):
        
#         idx = np.where((B_matrix_weighted_array[:, 0] == path[i]) & (B_matrix_weighted_array[:, 1] == path[i+1]))[0]

#         if len(idx) > 0:
#             B_matrix_weighted_array[idx[0], 6] = B_matrix_weighted_array[idx[0], 6] + row['S000_adjusted']
#             B_matrix_weighted_array[idx[0], 7] = B_matrix_weighted_array[idx[0], 7] + row['SA01_adjusted']
#             B_matrix_weighted_array[idx[0], 8] = B_matrix_weighted_array[idx[0], 8] + row['SA02_adjusted']
#             B_matrix_weighted_array[idx[0], 9] = B_matrix_weighted_array[idx[0], 9] + row['SA03_adjusted']
#             B_matrix_weighted_array[idx[0], 10] = B_matrix_weighted_array[idx[0], 10] + row['SE01_adjusted']
#             B_matrix_weighted_array[idx[0], 11] = B_matrix_weighted_array[idx[0], 11] + row['SE02_adjusted']
#             B_matrix_weighted_array[idx[0], 12] = B_matrix_weighted_array[idx[0], 12] + row['SE03_adjusted']
#             B_matrix_weighted_array[idx[0], 13] = B_matrix_weighted_array[idx[0], 13] + row['SI01_adjusted']
#             B_matrix_weighted_array[idx[0], 14] = B_matrix_weighted_array[idx[0], 14] + row['SI02_adjusted']
#             B_matrix_weighted_array[idx[0], 15] = B_matrix_weighted_array[idx[0], 15] + row['SI03_adjusted']
#         elif len(idx) == 0:
#             idx = np.where((B_matrix_weighted_array[:, 1] == path[i]) & (B_matrix_weighted_array[:, 0] == path[i+1]))[0]
#             if len(idx) > 0:
#                 B_matrix_weighted_array[idx[0], 6] = B_matrix_weighted_array[idx[0], 6] + row['S000_adjusted']
#                 B_matrix_weighted_array[idx[0], 7] = B_matrix_weighted_array[idx[0], 7] + row['SA01_adjusted']
#                 B_matrix_weighted_array[idx[0], 8] = B_matrix_weighted_array[idx[0], 8] + row['SA02_adjusted']
#                 B_matrix_weighted_array[idx[0], 9] = B_matrix_weighted_array[idx[0], 9] + row['SA03_adjusted']
#                 B_matrix_weighted_array[idx[0], 10] = B_matrix_weighted_array[idx[0], 10] + row['SE01_adjusted']
#                 B_matrix_weighted_array[idx[0], 11] = B_matrix_weighted_array[idx[0], 11] + row['SE02_adjusted']
#                 B_matrix_weighted_array[idx[0], 12] = B_matrix_weighted_array[idx[0], 12] + row['SE03_adjusted']
#                 B_matrix_weighted_array[idx[0], 13] = B_matrix_weighted_array[idx[0], 13] + row['SI01_adjusted']
#                 B_matrix_weighted_array[idx[0], 14] = B_matrix_weighted_array[idx[0], 14] + row['SI02_adjusted']
#                 B_matrix_weighted_array[idx[0], 15] = B_matrix_weighted_array[idx[0], 15] + row['SI03_adjusted']
#         if idx[0]not in pairlist_test_1:
#             pairlist_test_1.append(idx[0])

# end=time.time()

# print(end-start)
# print('Number of updates from Approach 1: ' + str(sum(B_matrix_weighted_array[:, 6] != 0)))

# if sum(B_matrix_weighted_array[:, 6] != 0) == len(pairlist_actual):
#     print('Approach 1 update count matches expected update count.')

# --------------------------------------------------------------------

# Approach 2: Converting B_matrix_weighted to a dictionary for faster lookups (O(1) lookups, faster)

# Convert B_matrix_weighted_array to a dictionary for faster lookups
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

with open('B_matrix_weighted_updated.pickle', 'wb') as handle:
    pickle.dump(B_matrix_weighted_array, handle, protocol=pickle.HIGHEST_PROTOCOL)