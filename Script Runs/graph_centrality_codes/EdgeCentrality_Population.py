#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 07:39:48 2022

@author: debasishjana
"""

import pickle
import numpy
import matplotlib.pyplot as plt

import networkx as nx

import numpy as np

import scipy.io as sio
import pandas as pd


import matplotlib.colors as mcolors

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
    plt.savefig('EdgeCentrality_degree_popWt_Plot.eps', format='eps')
    plt.show()


# # open a file, where you stored the pickled data
# file = open('nodes_edges_weighted.pickle', 'rb')

# # dump information to that file
# data = pickle.load(file)

# # close the file
# file.close()


# # open a file, where you stored the pickled data
# file0 = open('nodes_edges.pickle', 'rb')

# # dump information to that file
# data0 = pickle.load(file0)

# # close the file
# file0.close()

with open(r'nodes_edges_weighted.pickle', 'rb') as handle:
    B_matrix_sliced,nodes_coordinates_array = pickle.load(handle)
    

# B_matrix_sliced is the edge informations
# nodes_coordinates_array is the node information
    
    
Hillside_edgelist = B_matrix_sliced[:,0:2]
NetworkEdgeWt_pre = B_matrix_sliced[:,5]
temp = np.reciprocal(NetworkEdgeWt_pre)
temp[temp == np.inf] = 2500
temp = np.expand_dims(temp, axis = 1)

FinalEdge = np.concatenate((Hillside_edgelist, temp), axis = 1)
FinalEdge_df = pd.DataFrame(FinalEdge, columns = ['from', 'to', 'weight'])

G = nx.from_pandas_edgelist(FinalEdge_df, source = 'from', target = 'to', edge_attr = True)



EdgeCentrality_degree_popWt = nx.edge_betweenness_centrality(G, weight = 'weight')
    
# G = nx.Graph()
# G.add_edges_from(Hillside_edgelist, weight = temp)    
    
Hillside_NodeCoordinate = nodes_coordinates_array[:,0:2]

d = dict(enumerate(Hillside_NodeCoordinate, 0))

# # subax1 = plt.figure(num=1, figsize=(10,6))
# # nx.draw(G, pos=d, node_color='r', edge_color='b', node_size=0.01, width=0.1)
# # # plt.savefig('LAStreets.eps', format='eps')




subax5 = plt.figure(num=5, figsize=(10,6))
edge_draw(G, d, EdgeCentrality_degree_popWt, 'edge betweenness centrality with population weight')

    
# create a binary pickle file 
f = open("EdgeCentrality_degree_popWt_save.pkl","wb")

# write the python object (dict) to pickle file
pickle.dump(EdgeCentrality_degree_popWt,f)

# close file
f.close()







   
    
