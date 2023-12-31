import numpy as np
import matplotlib.pyplot as plt
from Utils.scoring import scoring
from Utils.borda_count import bordaCount
from Utils.condorcet import condorcet
from Utils.instant_runoff import instant_runoff
from Utils.discrepancyFunction import discrepancy
from Utils.plurality import plurality
from Utils.Dictatorship import dictatorship
from Utils.jack_knife import JackKnife


def distance(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


n_points = 10000
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


# Adds n candidates each a set distance from the centroid
for i in range(n_candidates):
    theta = np.random.uniform(0, 2 * np.pi)
    D = i * (10 / (n_candidates - 1))
    candidate_i = [mean_x + D * np.cos(theta), mean_y + D * np.sin(theta)]
    candidates.update({i: candidate_i})

ballot_box = {}

# Creates a Ballot for each voter that contains the ir ordered ranking of candidates. The Ballot Box is
# a dictionary containing both the coordinates of a given voter and their ballot.
for i in range(len(coordinates)):
    ballot = list(range(n_candidates))
    ballot_new = []
    for j in ballot:
        ballot_new.append(distance(candidates[j], coordinates[i]))
    ballot_fin = np.column_stack((ballot, ballot_new))
    ballot_fin_n = np.argsort(ballot_fin, axis=0)
    ballot_box.update({i: {"coordinates": coordinates[i], "vote": ballot_fin[ballot_fin_n[:, 1]]}})

# print(ballot_box[3]["vote"])
# This is my braindead way of getting candidate coordinates into an array so I can plot them
candidate_array = np.array(list(candidates.values()))

# Calculate distances from each point to the candidate point
# distances = np.sqrt(np.sum((coordinates - candidate_point) ** 2, axis=1))

# Makes a colormap with three colours
colormap = np.array(['slateblue', 'limegreen', 'gold'])

categories = np.array([])

for i in range(len(coordinates)):
    cat = ballot_box[i]["vote"][0][0]
    categories = np.append(categories, [cat])

categories = categories.astype(int)

# Plot the points and their distances
plt.scatter(x_coords, y_coords, c=colormap[categories])
plt.scatter(candidate_array[:, 0], candidate_array[:, 1], marker='o', color='red', label='Candidate')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
#plt.show()



print('plurality:', plurality(ballot_box))
print('instant run off:', instant_runoff(ballot_box))
print('borda count:', bordaCount(ballot_box, n_candidates))
print('condorcet:', condorcet(ballot_box, n_candidates))
print('scoring:', scoring(ballot_box, n_candidates))
print('dictatorship:', dictatorship(ballot_box))
print()






