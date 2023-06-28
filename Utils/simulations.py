import numpy as np
from show_grid import distance
from Utils.discrepancyFunction import discrepancy

from Utils.plurality import plurality
from Utils.instant_runoff import instant_runoff
from Utils.borda_count import bordaCount
from Utils.condorcet import condorcet
from Utils.scoring import scoring
from Utils.Dictatorship import dictatorship
from Utils.Stability import stability


def voters(n_points, x_range, y_range):
    x_coords = np.random.uniform(x_range[0], x_range[1], n_points)
    y_coords = np.random.uniform(y_range[0], y_range[1], n_points)
    return np.column_stack((x_coords, y_coords))


def voters_normal(n_points, mean, stdev):
    x_coords = np.random.normal(mean[0], stdev[0], n_points)
    y_coords = np.random.normal(mean[1], stdev[1], n_points)
    return np.column_stack((x_coords, y_coords))


def voters_bimodal(n_points, mean_1, mean_2, stdev_1, stdev_2):
    x_coords = np.random.normal(mean_1[0], stdev_1[0], n_points/2)
    y_coords = np.random.normal(mean_1[1], stdev_1[1], n_points/2)
    x_coords = np.append(x_coords, np.random.normal(mean_2[0], stdev_2[0], n_points/2))
    y_coords = np.append(y_coords, np.random.normal(mean_2[1], stdev_2[1], n_points / 2))
    return np.column_stack((x_coords, y_coords))


num_candidates = 10
votersCoords = voters(1000, (-10, 10), (-10, 10))


def Candidates(voters_coords, n_candidates):
    candidates = {}
    for i in range(n_candidates):
        theta = np.random.uniform(0, 2 * np.pi)
        D = i * (10 / (n_candidates - 1))
        mean_x = voters_coords[:, 0].mean()
        mean_y = voters_coords[:, 1].mean()
        candidate_i = [mean_x + D * np.cos(theta), mean_y + D * np.sin(theta)]
        candidates.update({i: candidate_i})
    return candidates


def Candidates_rand(n_candidates, x_range, y_range):
    candidates = {}
    for i in range(n_candidates):
        candidate_i = [np.random.uniform(x_range[0], x_range[1]), np.random.uniform(y_range[0], y_range[1])]
        candidates.update({i: candidate_i})
    return candidates

def Candidates_norm(n_candidates, mean, stdev):
    candidates = {}
    for i in range(n_candidates):
        candidate_i = [np.random.normal(mean[0], stdev[0]), np.random.normal(mean[1], stdev[1])]
        candidates.update({i: candidate_i})
    return candidates


def Candidates_no_centre(voters_coords, n_candidates):
    candidates = {}
    for i in range(n_candidates):
        theta = np.random.uniform(0, 2 * np.pi)
        D = (i+1) * (10 / n_candidates)
        mean_x = voters_coords[:, 0].mean()
        mean_y = voters_coords[:, 1].mean()
        candidate_i = [mean_x + D * np.cos(theta), mean_y + D * np.sin(theta)]
        candidates.update({i: candidate_i})
    return candidates


def simulation(voters_coords, n_candidates, repeats, voting_systems):
    results = []
    ideal_candidate = [voters_coords[:, 0].mean(), voters_coords[:, 1].mean()]
    avg_discrepancy = {votingSystem.__name__: 0 for votingSystem in voting_systems}

    for repeat in range(repeats):
        candidates = Candidates_no_centre(voters_coords, n_candidates)

        ballot_box = {}
        for i in range(len(voters_coords)):
            ballot = list(range(n_candidates))
            ballot_new = []
            for j in ballot:
                ballot_new.append(distance(candidates[j], voters_coords[i]))
            ballot_fin = np.column_stack((ballot, ballot_new))
            ballot_fin_n = np.argsort(ballot_fin, axis=0)
            ballot_box.update({i: {"coordinates": voters_coords[i], "vote": ballot_fin[ballot_fin_n[:, 1]]}})

        data = {}
        for votingSystem in voting_systems:
            winners = list(votingSystem(ballot_box, n_candidates).keys())
            winner = winners[0]
            discrepancy_val = discrepancy(votingSystem, ballot_box, ideal_candidate, candidates, n_candidates)
            data[votingSystem.__name__] = {"Winner": winner, "Discrepancy": discrepancy_val}
            # average discrepancy
            avg_discrepancy[votingSystem.__name__] += discrepancy_val / repeats

        results.append(data)

    return results, avg_discrepancy


votingSystems_list = [plurality, instant_runoff, bordaCount, condorcet, scoring, dictatorship]
Simulation, avg_Discrepancy = simulation(votersCoords, num_candidates, 2, votingSystems_list)

for repeat, (result, discrepancy) in enumerate(zip(Simulation,avg_Discrepancy), start=1):
    print("Repeat:", repeat)
    for votingSystem, data in result.items():
        print(votingSystem, ":", data, end="\n")
    print()
print('average discrepancies:', avg_Discrepancy)
