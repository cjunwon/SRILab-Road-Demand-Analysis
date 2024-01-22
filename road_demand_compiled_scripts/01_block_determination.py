import geopandas as gpd
import pandas as pd
import numpy as np
import pickle
from shapely import Point
from shapely.ops import nearest_points
from rtree import index

# Import and subset block data
blocks = gpd.read_file('blocks/tl_2020_06037_tabblock20.shp')
blocknumbers = np.array(blocks["GEOID20"],dtype=str)
blockboundaries = np.array(blocks["geometry"])

nodes_edges_weighted = pd.read_pickle('graph_centrality_codes/nodes_edges_weighted.pickle')
B_matrix_weighted, node_coordinates_weighted = nodes_edges_weighted
Hillside_NodeCoordinate = node_coordinates_weighted[:,0:2]

# Check if blockboundaries and blocknumbers are the same length
if len(blockboundaries) != len(blocknumbers):
    print("Error: Length of blockboundaries and blocknumbers do not match")

# Create an R-tree index
idx = index.Index()
for i, boundary in enumerate(blockboundaries):
    idx.insert(i, boundary.bounds)

# Initialize empty lists to store node and block information
Node_Block = []
Unidentified_Nodes = []

# Identify nodes that are in a block using R-tree
for i in range(len(Hillside_NodeCoordinate)):
    coord = Hillside_NodeCoordinate[i]
    possible_blocks = list(idx.intersection((coord[0], coord[1], coord[0], coord[1])))
    for block_idx in possible_blocks:
        if blockboundaries[block_idx].contains(Point(coord[0], coord[1])):
            Node_Block.append([i, blocknumbers[block_idx], blockboundaries[block_idx]])

Identified_Nodes = np.array([row[0] for row in Node_Block])
total_nodes_identified = len(Node_Block)
total_nodes_out_of_bounds = len(Hillside_NodeCoordinate) - total_nodes_identified
extracted_blocknumbers = np.array([item[1] for item in Node_Block])
unique_blocknumbers = np.unique(extracted_blocknumbers)
unique_blocknumbers_count = len(unique_blocknumbers)

print("Total nodes identified: " + str(total_nodes_identified), "\nNodes out of bounds: " + str(total_nodes_out_of_bounds), "\nUnique blocknumbers: " + str(unique_blocknumbers_count))

# Make a list with the first element in Node_Block
Identified_Nodes_Index = [item[0] for item in Node_Block]

# Identify nodes that are not in any block
for i in range(len(Hillside_NodeCoordinate)):
    if i not in Identified_Nodes:
        Unidentified_Nodes.append(i)

print('Nodes without block placement: ' + str(Unidentified_Nodes))

# Identify the closest block for each node that is not in any block
for i in Unidentified_Nodes:
    closest_block = min(blockboundaries, key=lambda x: x.distance(Point(Hillside_NodeCoordinate[i][0], Hillside_NodeCoordinate[i][1])))
    closest_block_idx = np.where(blockboundaries == closest_block)
    closest_block_number = blocknumbers[closest_block_idx]
    print('Node coordinate ' + str(i) + ' with coordinates ' + str(Hillside_NodeCoordinate[i]) + ' is closest to block ' + str(closest_block_number))
    Node_Block.insert(i, [i, closest_block_number, closest_block])

# Check if all nodes have been identified
total_nodes_identified = len(Node_Block)

print("Total nodes identified: " + str(total_nodes_identified))

# Save Node_Block as a pickle file
with open(r'intermediate_files/Node_Block.pkl', 'wb') as f:
    pickle.dump(Node_Block, f)