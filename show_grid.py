import numpy as np
import matplotlib.pyplot as plt

n_points = 100
n_candidates = 3
x_range = (-10, 10)
y_range = (-10, 10)

x_coords = np.random.uniform(x_range[0], x_range[1], n_points)
y_coords = np.random.uniform(y_range[0], y_range[1], n_points)

coordinates = np.column_stack((x_coords, y_coords))

candidates = {}
mean_x = x_coords.mean()
mean_y = y_coords.mean()
candidate_point = [mean_x, mean_y]

for i in range(n_candidates):
    theta = np.random.uniform(0, 2*np.pi)
    D = i*(10/(n_candidates - 1))
    candidate_i = [mean_x + D*np.cos(theta), mean_y + D*np.sin(theta)]
    candidates.update({i: candidate_i})

def Distance(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

ballot_box = {}

for i in range(len(coordinates)):
    ballot = list(range(n_candidates))
    ballot_new = []
    for j in ballot:
        ballot_new.append(Distance(candidates[j], coordinates[i]))
    ballot_fin = np.column_stack((ballot, ballot_new))
    ballot_fin_n = np.argsort(ballot_fin, axis=0)
    ballot_box.update({i: {"coordinates": coordinates[i], "vote": ballot_fin[ballot_fin_n[:,1]]}})

print(ballot_box[3]["vote"])


# Calculate distances from each point to the candidate point
# distances = np.sqrt(np.sum((coordinates - candidate_point) ** 2, axis=1))

# Plot the points and their distances
# plt.scatter(x_coords, y_coords)
# plt.scatter(candidate_point[0], candidate_point[1], marker='o', color='red', label='Candidate')
# plt.legend()
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.grid(True)
# plt.show()
