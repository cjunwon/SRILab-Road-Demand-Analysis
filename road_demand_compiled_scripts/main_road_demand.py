import subprocess

# 00 - Package Installation

'''

This section installs the required packages for the script to run.
If there are missing packages, the script will install them with pip3.
You can change pip3 to other package managers like pipenv or conda.

Before running this script, make sure you are in the 'road_demand_compiled_scripts' directory.

'''

required_packages = [
    'numpy',
    'matplotlib',
    'requests',
    'networkx',
    'scipy',
    'pandas',
    'geopandas',
    'shapely',
    'rtree',
    'scikit-gstat'
]

def check_and_install_with_pip(package):
    try:
        subprocess.run(['pip3', 'show', package], check=True, stdout=subprocess.PIPE)
        print(f"{package} is already installed with pip3.")
    except subprocess.CalledProcessError:
        print(f"{package} is not installed with pip3. Installing...")
        subprocess.run(['pip3', 'install', package], check=True)

# Check and install required packages
for package in required_packages:
    check_and_install_with_pip(package)

#######################################################################################################################

# Running each script in sequence:

# 01 -  Block Determination
'''
Description: This script determines which block each node is in.

Input:
    - blocks/tl_2020_06037_tabblock20.shp
    - graph_centrality_codes/nodes_edges_weighted.pickle

Output:
    - intermediate_files/Node_Block.pkl

'''
subprocess.run(['python', '01_block_determination.py'])

# 02 - Block Node Pairing
'''
Description: This script combines results from 01_block_determination.py with the Origin-Destination dataset to append job/worker quantity for each node.

Input:
    - lodes_od_data/ca_od_main_JT00_2020.csv
    - intermediate_files/Node_Block.pkl

Output:
    - intermediate_files/Origin_Destination_Node_Added.pkl

'''
subprocess.run(['python', '02_block_node_pairing.py'])

# 03 - Shortest Path
'''
Description: This script implements shortest path (single_source_dijkstra_path) algorithm to approximate optimal traveling path between two nodes.

Input:
    - graph_centrality_codes/nodes_edges_weighted.pickle
    - graph_centrality_codes/distance.pickle
    - intermediate_files/Origin_Destination_Node_Added.pkl

Output:
    - intermediate_files/Shortest_Path_Results.pkl

'''
subprocess.run(['python', '03_shortest_path.py'])

# 04 - Path Usage
'''
Description: This script computes road demand based on results from 03_shortest_path.py by couting pairing frequency of nodes.

Input:
    - graph_centrality_codes/nodes_edges_weighted.pickle
    - intermediate_files/Shortest_Path_Results.pkl

Output:
    - intermediate_files/B_matrix_weighted_updated.pickle

'''
subprocess.run(['python', '04_path_usage.py'])

# 05 - Kriging Update
'''
Description: This script updates missing road demand values using kriging.

Input:
    - udf/hillside_inventory_LA_centrality_full_new_evacmidnorth_lodes.geojson

Output:
    - udf/hillside_inventory_LA_centrality_full_new_evacmidnorth_lodes_kriging.geojson

'''
subprocess.run(['python', '05_kriging_update.py'])
