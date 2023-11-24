import numpy as np
import geopandas as gpd
import pickle

from skgstat import Variogram, OrdinaryKriging
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

udf=gpd.read_file(r"hillside_inventory_LA_centrality_full_new_evacmidnorth_lodes.geojson")

udf_before = udf.copy()

# print(udf.columns)

# print(udf['Street_Designation'].unique())
# print(len(udf['Street_Designation'].unique()))

for designation in udf['Street_Designation'].unique():
    print(designation)

# S000_adjusted

for designation in udf['Street_Designation'].unique():
    print(designation)
    x1 = udf[(udf['Street_Designation'] == designation) & (udf['S000_adjusted'] != 0)]['centroid_lat'].to_numpy()
    y1 = udf[(udf['Street_Designation'] == designation) & (udf['S000_adjusted'] != 0)]['centroid_lon'].to_numpy()
    z_S000 = udf[(udf['Street_Designation'] == designation) & (udf['S000_adjusted'] != 0)]['S000_adjusted'].to_numpy()

    x2 = udf[(udf['Street_Designation'] == designation) & (udf['S000_adjusted'] == 0)]['centroid_lat'].to_numpy()
    y2 = udf[(udf['Street_Designation'] == designation) & (udf['S000_adjusted'] == 0)]['centroid_lon'].to_numpy()

    if len(x1) == 0:
        print("No data for designation: ", designation)

    else:
        if len(np.unique(z_S000)) == 1:
            print("All values in z1 are constant for designation: ", designation)
        else:
            print("Values in z1 are not constant.")
            variogram_model_S000 = Variogram(np.vstack((x1, y1)).T, z_S000)

            ok_S000 = OrdinaryKriging(variogram_model_S000, min_points=2, max_points=10, mode='exact')

            field_S000 = ok_S000.transform(x2, y2)

            print(str(len(field_S000)) + " values in field for designation: ", designation)
            print(str(len(x2)) + " should ideally be updated for designation: ", designation)

            # norm = Normalize(vmin=min(np.min(z1), np.min(field)), vmax=max(np.max(z1), np.max(field)))

            if len(x2) == len(field_S000):
                print("Lengths match for designation: ", designation)
                for i in range(len(x2)):
                    udf.loc[(udf['centroid_lat'] == x2[i]) & (udf['centroid_lon'] == y2[i]), 'S000_adjusted'] = field_S000[i]

            else:
                print("Lengths do not match for designation: ", designation)
                # for i in range(len(x2)):
                #     udf.loc[(udf['centroid_lat'] == x2[i]) & (udf['centroid_lon'] == y2[i]), 'S000_adjusted'] = field_S000[i]

print("Before Kriging - number of rows with 0 in S000_adjusted: ", len(udf_before[(udf_before['S000_adjusted'] == 0)]))
print("After Kriging - number of rows with 0 in S000_adjusted: ", len(udf[(udf['S000_adjusted'] == 0)]))

# All other adjusted columns

adj_cols = ['SA01_adjusted', 'SA02_adjusted', 'SA03_adjusted', 'SE01_adjusted', 'SE02_adjusted', 'SE03_adjusted', 'SI01_adjusted', 'SI02_adjusted', 'SI03_adjusted']

for col in adj_cols:
    print("Currently updating: ", col)
    for designation in udf['Street_Designation'].unique():
        print(designation)
        x1 = udf[(udf['Street_Designation'] == designation) & (udf[col] != 0)]['centroid_lat'].to_numpy()
        y1 = udf[(udf['Street_Designation'] == designation) & (udf[col] != 0)]['centroid_lon'].to_numpy()
        z1 = udf[(udf['Street_Designation'] == designation) & (udf[col] != 0)][col].to_numpy()

        x2 = udf[(udf['Street_Designation'] == designation) & (udf[col] == 0)]['centroid_lat'].to_numpy()
        y2 = udf[(udf['Street_Designation'] == designation) & (udf[col] == 0)]['centroid_lon'].to_numpy()

        if len(x1) == 0:
            print("No data for designation: ", designation)

        else:
            if len(np.unique(z1)) == 1:
                print("All values in z1 are constant for designation: ", designation)
            else:
                print("Values in z1 are not constant.")
                variogram_model = Variogram(np.vstack((x1, y1)).T, z1)

                ok = OrdinaryKriging(variogram_model, min_points=2, max_points=10, mode='exact')

                field = ok.transform(x2, y2)

                print(str(len(field)) + " values in field for designation: ", designation)
                print(str(len(x2)) + " should ideally be updated for designation: ", designation)

                # norm = Normalize(vmin=min(np.min(z1), np.min(field)), vmax=max(np.max(z1), np.max(field)))

                if len(x2) == len(field):
                    print("Lengths match for designation: ", designation)
                    for i in range(len(x2)):
                        udf.loc[(udf['centroid_lat'] == x2[i]) & (udf['centroid_lon'] == y2[i]), col] = field[i]

                else:
                    print("Lengths do not match for designation: ", designation)

udf.to_file(r"hillside_inventory_LA_centrality_full_new_evacmidnorth_lodes_kriging.geojson", driver='GeoJSON')