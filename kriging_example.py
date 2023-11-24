import numpy as np
from skgstat import Variogram, OrdinaryKriging
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
# Example data
x1 = np.random.rand(100)  # replace with your actual x1 values
y1 = np.random.rand(100)  # replace with your actual y1 values
z1 = np.random.rand(100)  # replace with your actual z values

x2 = np.random.rand(10)  # replace with your actual x2 values
y2 = np.random.rand(10)  # replace with your actual y2 values

# Create a variogram model
variogram_model = Variogram(np.vstack((x1, y1)).T, z1)

# Plot the experimental variogram
# variogram_model.plot()
# plt.show()

# Use the variogram model for ordinary kriging
ok = OrdinaryKriging(variogram_model, min_points=3, max_points=5, mode='exact')

field = ok.transform(x2, y2)

norm = Normalize(vmin=min(np.min(z1), np.min(field)), vmax=max(np.max(z1), np.max(field)))

# Plotting the results
scatter1=plt.scatter(x1, y1, c=z1,norm=norm,marker='o', label='Sampled Points')
scatter2=plt.scatter(x2, y2, c=field,norm=norm, marker='x', label='Kriging Predictions')

cbar = plt.colorbar(scatter1, label='Z Values')
cbar2 = plt.colorbar(scatter2, label='Z Values')
plt.legend()
plt.show()

