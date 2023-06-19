import numpy as np
import matplotlib.pyplot as plt

n_points = 100
x_range = (-10, 10)
y_range = (-10, 10)
candidate_point = (0, 0)

x_coords = np.random.uniform(x_range[0], x_range[1], n_points)
y_coords = np.random.uniform(y_range[0], y_range[1], n_points)

coordinates = np.column_stack((x_coords, y_coords))

# Calculate distances from each point to the candidate point
distances = np.sqrt(np.sum((coordinates - candidate_point) ** 2, axis=1))

# Plot the points and their distances
plt.scatter(x_coords, y_coords, c=distances, cmap='viridis')
plt.colorbar(label='Distance')
plt.scatter(candidate_point[0], candidate_point[1], marker='o', color='red', label='Candidate')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
