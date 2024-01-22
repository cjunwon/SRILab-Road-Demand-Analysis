import pandas as pd
import pickle

'''
Block to block travel population column representations:

Total number of jobs:   S000
Age columns:            SA01, SA02, SA03 (all sum to S000)
Income columns:         SE01, SE02, SE03 (all sum to S000)
Industry columns:       SI01, SI02, SI03 (all sum to S000)
'''

# Read in data
Origin_Destination = pd.read_csv('lodes_od_data/ca_od_main_JT00_2020.csv')

# Nodes with matching blocks (from 01_block_determination.py)
with open(r'intermediate_files/Node_Block.pkl', 'rb') as f:
    Node_Block = pickle.load(f)


# print(Origin_Destination.head())

# # Show unique values in the 'S000' column
# print(Origin_Destination['S000'].unique())

Initial_Origin_Destination_Count = len(Origin_Destination)

# Create dictionary for block and node pairings (identified from BlockDetermination.ipynb)
block_node_dict = {}

# Iterate over the list and add the block ids and node coordinates to the dictionary
for node_id, block_id, block_coord in Node_Block:
    if int(block_id) not in block_node_dict:
        block_node_dict[int(block_id)] = []
    block_node_dict[int(block_id)].append(node_id)

Origin_Destination_Node_Added = Origin_Destination.copy()

# Map nodes to work and home blocks
Origin_Destination_Node_Added['w_node_id'] = Origin_Destination_Node_Added['w_geocode'].map(block_node_dict)
Origin_Destination_Node_Added['h_node_id'] = Origin_Destination_Node_Added['h_geocode'].map(block_node_dict)

# Remove rows where the node columns are missing (i.e. the block is not in the node dictionary)
Origin_Destination_Node_Added = Origin_Destination_Node_Added[Origin_Destination_Node_Added['w_node_id'].notnull()]
Origin_Destination_Node_Added = Origin_Destination_Node_Added[Origin_Destination_Node_Added['h_node_id'].notnull()]

# Explode the node columns so that each row has a single node coordinate
Origin_Destination_Node_Added = Origin_Destination_Node_Added.explode('w_node_id')
Origin_Destination_Node_Added = Origin_Destination_Node_Added.explode('h_node_id')

# Keep track of the number of unique block combinations and node combinations
Unique_Block_Combinations_Count = len(Origin_Destination_Node_Added.index.unique())
Unique_Node_Combinations_Count = len(Origin_Destination_Node_Added)

# Shift node coordinate column locations
Origin_Destination_Node_Added.insert(1, 'w_node_id', Origin_Destination_Node_Added.pop('w_node_id'))
Origin_Destination_Node_Added.insert(3, 'h_node_id', Origin_Destination_Node_Added.pop('h_node_id'))

# print(Origin_Destination_Node_Added.head())

# check if there are any rows where w_geocode and h_geocode are the same
same_code = Origin_Destination_Node_Added[Origin_Destination_Node_Added['w_geocode'] == Origin_Destination_Node_Added['h_geocode']]
print('Number of rows where w_geocode == h_geocode: ', len(same_code))

# check if there are any rows where w_node_id and h_node_id are the same
same_id = Origin_Destination_Node_Added[Origin_Destination_Node_Added['w_node_id'] == Origin_Destination_Node_Added['h_node_id']]
print('Number of rows where w_node_id == h_node_id: ',len(same_id))

# Remove rows where w_node_id and h_node_id are the same
Origin_Destination_Node_Added = Origin_Destination_Node_Added[Origin_Destination_Node_Added['w_node_id'] != Origin_Destination_Node_Added['h_node_id']]

Unique_Node_Combinations_Count_Final = len(Origin_Destination_Node_Added)


print('LODES dataset origin/destination block combination count: ' + str(Initial_Origin_Destination_Count) + '\nRelevant blocks combination count: ' + str(Unique_Block_Combinations_Count) + '\nRelevant nodes combination count: ' + str(Unique_Node_Combinations_Count) + '\nRelevant nodes combination count (same node to node removed): ' + str(Unique_Node_Combinations_Count_Final))

# Count where 'w_geocode' and 'h_geocode' are uniquely paired
Origin_Destination_Node_Added['unique_pair'] = Origin_Destination_Node_Added['w_geocode'].astype(str) + Origin_Destination_Node_Added['h_geocode'].astype(str)

# Count how many times each unique pair appears, and add it as a column
Origin_Destination_Node_Added['unique_pair_count'] = Origin_Destination_Node_Added.groupby('unique_pair')['unique_pair'].transform('count')

# List of column names to be adjusted
cols_to_adjust = ['S000', 'SA01', 'SA02', 'SA03', 'SE01', 'SE02', 'SE03', 'SI01', 'SI02', 'SI03']

# Iterate over the columns and create new adjusted columns
for col in cols_to_adjust:
    Origin_Destination_Node_Added[f'{col}_adjusted'] = Origin_Destination_Node_Added[col] / Origin_Destination_Node_Added['unique_pair_count']

# Print column names of the dataframe
print('Column names of new dataframe: ', Origin_Destination_Node_Added.columns)

# Dump Origin_Destination_Node_Added_Final as a pickle file
Origin_Destination_Node_Added.to_pickle('intermediate_files/Origin_Destination_Node_Added.pkl')

# Export updated csv
# Origin_Destination_Node_Added.to_csv('ca_od_main_JT00_2020_Node_Added.csv', index=False)