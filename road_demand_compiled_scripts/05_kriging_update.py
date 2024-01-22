import numpy as np
import geopandas as gpd
import pickle
from skgstat import Variogram, OrdinaryKriging
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# Import udf (updated dataframe)
udf=gpd.read_file(r"udf/hillside_inventory_LA_centrality_full_new_evacmidnorth_lodes.geojson")

udf_before = udf.copy()

# print(udf.columns)
# print(udf['Street_Designation'].unique())
# print(len(udf['Street_Designation'].unique()))

print('Potential Designations: \n')
for designation in udf['Street_Designation'].unique():
    print(designation)

# Define columns to be updated
adj_cols = ['SA01_adjusted', 'SA02_adjusted', 'SA03_adjusted', 'SE01_adjusted', 'SE02_adjusted', 'SE03_adjusted', 'SI01_adjusted', 'SI02_adjusted', 'SI03_adjusted', 'S000_adjusted']

# Apply kriging to update values in adj_cols based on whether S000_adjusted == 0
for col in adj_cols:
    print("\n Currently updating: ", col)
    for designation in udf['Street_Designation'].unique():
        print(designation)
        # Set x1, y1, z1 for existing points
        x1 = udf[(udf['Street_Designation'] == designation) & (udf['S000_adjusted'] != 0)]['centroid_lat'].to_numpy()
        y1 = udf[(udf['Street_Designation'] == designation) & (udf['S000_adjusted'] != 0)]['centroid_lon'].to_numpy()
        z1 = udf[(udf['Street_Designation'] == designation) & (udf['S000_adjusted'] != 0)][col].to_numpy()

        # Set x2, y2 for points to be updated (with S000_adjusted == 0)
        x2 = udf[(udf['Street_Designation'] == designation) & (udf['S000_adjusted'] == 0)]['centroid_lat'].to_numpy()
        y2 = udf[(udf['Street_Designation'] == designation) & (udf['S000_adjusted'] == 0)]['centroid_lon'].to_numpy()

        # Error handling
        if len(x1) == 0:
            print("\n No data for designation: ", designation)

        if len(z1) == 0:
            break

        else:
            # Error handling
            if len(np.unique(z1)) == 1:
                print("\n All values in z1 are constant for designation: ", designation)
            else:
                # We want z1 to be not constant for the variogram model to be created
                print("\n Values in z1 are not constant.")
                variogram_model = Variogram(np.vstack((x1, y1)).T, z1)

                # Apply Kriging to get field values for x2, y2
                ok = OrdinaryKriging(variogram_model, min_points=2, max_points=10, mode='exact')

                field = ok.transform(x2, y2)

                print(str(len(field)) + " values in field for designation: ", designation)
                print(str(len(x2)) + " should ideally be updated for designation: ", designation)
                
                ################################################################################################
                # Plotting Kriging predictions
                norm = Normalize(vmin=min(np.min(z1), np.min(field)), vmax=max(np.max(z1), np.max(field)))
                fig_name = str(col) + "_" + str(designation)

                plt.figure(fig_name, figsize=(20, 10))

                scatter1 = plt.scatter(x1, y1, c=z1, norm=norm, marker='o', label='Existing Points')
                scatter2 = plt.scatter(x2, y2, c=field, norm=norm, marker='x', s=200, label='Kriging Predictions')

                sample_label = 'Z Values (Existing) - ' + str(fig_name)
                kriging_label = 'Z Values (Kriging) - ' + str(fig_name)

                cbar = plt.colorbar(scatter1, label=sample_label)
                cbar2 = plt.colorbar(scatter2, label=kriging_label)
                plt.legend()
                plt.savefig("kriging_visuals/figure_" + str(fig_name) + ".png", format='png', dpi=200)
                # plt.show()
                ################################################################################################

                # Update udf with kriging predictions
                if len(x2) == len(field):
                    print("Lengths match for designation: ", designation)
                    for i in range(len(x2)):
                        udf.loc[(udf['centroid_lat'] == x2[i]) & (udf['centroid_lon'] == y2[i]), col] = field[i]

                else:
                    print("Lengths do not match for designation: ", designation)

print("Before Kriging - number of rows with 0 in S000_adjusted: ", len(udf_before[(udf_before['S000_adjusted'] == 0)]))
print("After Kriging - number of rows with 0 in S000_adjusted: ", len(udf[(udf['S000_adjusted'] == 0)]))

udf.to_file(r"udf/hillside_inventory_LA_centrality_full_new_evacmidnorth_lodes_kriging.geojson", driver='GeoJSON')