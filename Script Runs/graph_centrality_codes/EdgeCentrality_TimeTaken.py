#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 15:12:13 2022

@author: debasishjana
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import networkx as nx
import scipy.io as sio
import matplotlib.colors as mcolors
import pandas as pd

def draw(G, pos, measures, measure_name):
    
    nodes = nx.draw_networkx_nodes(G, pos, node_size=25, cmap=plt.cm.plasma, 
                                   node_color=list(measures.values()),
                                   nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    # labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos)

    plt.title(measure_name)
    plt.colorbar(nodes)
    plt.axis('off')
    plt.show()
    
    

def edge_draw(G, pos, measures, measure_name):
    nodes = nx.draw_networkx_nodes(G, pos, node_size=0)
    edges = nx.draw_networkx_edges(G, pos, width=0.1, edge_cmap=plt.cm.plasma,
                                   edge_color=list(measures.values()),
                                   edgelist=measures.keys())  
    # edges.set_norm(mcolors.SymLogNorm(linthresh=0, linscale=1, base=10))
    
    plt.title(measure_name)
    plt.colorbar(edges)
    plt.axis('off')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig('EdgeCentrality_degree_TimeWt_Plot.eps', format='eps')
    plt.show()


with open(r'nodes_edges_weighted.pickle', 'rb') as handle:
    B_matrix_weighted,node_coordinates_weighted = pickle.load(handle)
    
with open(r'distance.pickle', 'rb') as handle:
    distance_array = pickle.load(handle)  
    
#distance_array (1st col - distance (m), 2nd col - time (s), 3rd col - time in traffic (s))



Hillside_edgelist = B_matrix_weighted[:,0:2]
NetworkEdgeWt_pre = distance_array[:,2]
# NetworkEdgeWt_pre[NetworkEdgeWt_pre == 0] = 1

temp = np.expand_dims(NetworkEdgeWt_pre, axis = 1)

FinalEdge = np.concatenate((Hillside_edgelist, temp), axis = 1)
FinalEdge_df = pd.DataFrame(FinalEdge, columns = ['from', 'to', 'weight'])

G = nx.from_pandas_edgelist(FinalEdge_df, source = 'from', target = 'to', edge_attr = True)



EdgeCentrality_degree_TimeWt = nx.edge_betweenness_centrality(G, weight = 'weight')


# G = nx.Graph()
# G.add_edges_from(Hillside_edgelist, weight = NetworkEdgeWt_pre)    
    
Hillside_NodeCoordinate = node_coordinates_weighted[:,0:2]

d = dict(enumerate(Hillside_NodeCoordinate, 0))

# # subax1 = plt.figure(num=1, figsize=(10,6))
# # nx.draw(G, pos=d, node_color='r', edge_color='b', node_size=0.01, width=0.1)
# # # plt.savefig('LAStreets.eps', format='eps')


# EdgeCentrality_degree_TimeWt = nx.edge_betweenness_centrality(G, weight = 'weights')

subax5 = plt.figure(num=5, figsize=(10,6))
edge_draw(G, d, EdgeCentrality_degree_TimeWt, 'edge betweenness centrality with time taken weight')

    


# create a binary pickle file 
f = open("EdgeCentrality_degree_TimeWt_save.pkl","wb")

# write the python object (dict) to pickle file
pickle.dump(EdgeCentrality_degree_TimeWt,f)

# close file
f.close()




















