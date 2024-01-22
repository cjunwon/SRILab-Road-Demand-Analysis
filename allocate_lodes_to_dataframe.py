
import pickle
import numpy as np
# import matplotlib.pyplot as plt
# import networkx as nx
import geopandas as gpd
# import matplotlib.pyplot as plt
# import math
import numpy as np
# from shapely.geometry import Point, Polygon, LineString,MultiLineString
# import shapely.geometry
# import pandas as pd
import pickle
# import fiona
# from shapely.ops import linemerge
# import pyproj
# from functools import partial
# from shapely.ops import transform
# from geopy import distance
# gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
# from collections import defaultdict

# import pandas as pd
# import utm
# from scipy.spatial import KDTree


# import requests as req
# import re





with open(r'B_matrix_weighted_updated.pickle', 'rb') as handle:
    B_matrix_weighted_array= pickle.load(handle)    
    
sumarray=B_matrix_weighted_array[:,6].copy()
sumarray.sort()
sumarray_reversed=sumarray[::-1]

udf=gpd.read_file(r"hillside_inventory_LA_centrality_full_new_evacmidnorth.geojson")


sids=np.array(udf["SECT_ID"]).astype(int)
allocated_Bmatrix=np.zeros((len(sids),10))

exceptioncounter=0
for i in range(len(sids)):
    print(i)
    try:
        sid=sids[i]
        idx=np.where(B_matrix_weighted_array[:,2]==sid)[0][0]
        allocated_Bmatrix[i,:]=B_matrix_weighted_array[idx,6:16]
    except:
        exceptioncounter+=1
    
    

    
udf["S000_adjusted"]=allocated_Bmatrix[:,0]/np.max(allocated_Bmatrix[:,0])
udf["SA01_adjusted"]=allocated_Bmatrix[:,1]/np.max(allocated_Bmatrix[:,1])
udf["SA02_adjusted"]=allocated_Bmatrix[:,2]/np.max(allocated_Bmatrix[:,2])
udf["SA03_adjusted"]=allocated_Bmatrix[:,3]/np.max(allocated_Bmatrix[:,3])
udf["SE01_adjusted"]=allocated_Bmatrix[:,4]/np.max(allocated_Bmatrix[:,4])
udf["SE02_adjusted"]=allocated_Bmatrix[:,5]/np.max(allocated_Bmatrix[:,5])
udf["SE03_adjusted"]=allocated_Bmatrix[:,6]/np.max(allocated_Bmatrix[:,6])
udf["SI01_adjusted"]=allocated_Bmatrix[:,7]/np.max(allocated_Bmatrix[:,7])
udf["SI02_adjusted"]=allocated_Bmatrix[:,8]/np.max(allocated_Bmatrix[:,8])
udf["SI03_adjusted"]=allocated_Bmatrix[:,9]/np.max(allocated_Bmatrix[:,9])






sumarray_hs=allocated_Bmatrix[:,0].copy()

sumarray_hs.sort()
sumarray_hs_reversed=sumarray_hs[::-1]

udf.to_file(r"D:/Downloads/hillside_inventory_LA_centrality_full_new_evacmidnorth_lodes.geojson", driver='GeoJSON')