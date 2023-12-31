import numpy as np
import statistics
from show_grid import distance
from Utils.discrepancyFunction import discrepancy

from Utils.plurality import plurality
from Utils.instant_runoff import instant_runoff
from Utils.borda_count import bordaCount
from Utils.condorcet import condorcet
from Utils.scoring import scoring
from Utils.Dictatorship import dictatorship
from Utils.Stability import stability
from collections import defaultdict

#16 simulations to run in total for every type of voter & candidates

def voters(n_points, x_range, y_range):
    x_coords = np.random.uniform(x_range[0], x_range[1], n_points)
    y_coords = np.random.uniform(y_range[0], y_range[1], n_points)
    return np.column_stack((x_coords, y_coords))


def voters_normal(n_points, mean, stdev):
    x_coords = np.random.normal(mean[0], stdev[0], n_points)
    y_coords = np.random.normal(mean[1], stdev[1], n_points)
    return np.column_stack((x_coords, y_coords))


def voters_bimodal(n_points, mean_1, stdev_1, mean_2, stdev_2, ratio):
    x_coords = np.random.normal(mean_1[0], stdev_1[0], int(n_points*ratio))
    y_coords = np.random.normal(mean_1[1], stdev_1[1], int(n_points*ratio))
    x_coords = np.append(x_coords, np.random.normal(mean_2[0], stdev_2[0], int(n_points*(1-ratio))))
    y_coords = np.append(y_coords, np.random.normal(mean_2[1], stdev_2[1], int(n_points*(1-ratio))))
    return np.column_stack((x_coords, y_coords))


num_candidates = 10
votersCoords = [voters(1000, (-10,10), (-10,10)), voters_normal(1000, (0, 0), (5, 5)), voters_bimodal(1000, (5,0), (1,1), (-5,0), (1,1), 0.5), voters_bimodal(1000, (5,0), (1,5), (-5,0), (1,1), 0.5)]



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


def Candidates_norm(voters_coords, n_candidates, stdev):
    candidates = {}
    mean_x = voters_coords[:, 0].mean()
    mean_y = voters_coords[:, 1].mean()
    mean = [mean_x, mean_y]
    for i in range(n_candidates):
        candidate_i = [np.random.normal(mean[0], stdev[0]), np.random.normal(mean[1], stdev[1])]
        candidates.update({i: candidate_i})
    return candidates


def Candidates_bimodal(n_candidates, mean_1, stdev_1, mean_2, stdev_2, ratio):
    candidates = {}
    for i in range(int(n_candidates*ratio)):
        candidate_i = [np.random.normal(mean_1[0], stdev_1[0]), np.random.normal(mean_1[1], stdev_1[1])]
        candidates.update({i: candidate_i})
    for i in range(int(n_candidates*(1-ratio))):
        candidate_i = [np.random.normal(mean_2[0], stdev_1[0]), np.random.normal(mean_2[1], stdev_2[1])]
        candidates.update({i+int(n_candidates*ratio): candidate_i})
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
    avg_stability = {votingSystem.__name__: {} for votingSystem in voting_systems}

    for repeat in range(repeats):

        # candidates = Candidates(voters_coords, n_candidates)
        # candidates = Candidates_no_centre(voters_coords, n_candidates)
        candidates = Candidates_rand(n_candidates, (-10, 10), (-10, 10))
        # candidates = Candidates_norm(voters_coords, n_candidates, (5, 5))
        # candidates = Candidates_bimodal(n_candidates, (5,0), (1,1), (-5,0), (1,1))
        # candidates = Candidates_bimodal(n_candidates, (5,0), (1,5), (-5,0), (1,5))

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
            stability_val = stability(ballot_box, votingSystem, 1000, 0.1, n_candidates)
            data[votingSystem.__name__] = {"Winner": winner, "Discrepancy": discrepancy_val, "Stability": stability_val}
            # average discrepancy
            avg_discrepancy[votingSystem.__name__] += discrepancy_val / repeats
            for candidate, stabilityVal in stability_val.items():
                avg_stability[votingSystem.__name__].setdefault(candidate, []).append(stabilityVal)

        results.append(data)

    for votingSystem in voting_systems:
        for candidate_idx, candidate_stability_list in avg_stability[votingSystem.__name__].items():
            avg_stability[votingSystem.__name__][candidate_idx] = statistics.mean(candidate_stability_list)
    avg_stability2 = {
        key: np.mean(value) if isinstance(value, list) else value
        for key, value in avg_stability.items()
        }

    return results, avg_discrepancy, avg_stability2

repeats = 10
votingSystems_list = [plurality, instant_runoff, bordaCount, condorcet, scoring, dictatorship]
for v in votersCoords:
    Simulation, avg_Discrepancy = simulation(v, num_candidates, repeats, votingSystems_list)

    avg_Stability= {}
    avg_Stability= defaultdict(lambda: 0, avg_Stability)
    for i in Simulation:
        for key in i:
            avg_Stability[key] += max(i[key]['Stability'].values())/repeats

    print("Average Stability: ", avg_Stability)

# for repeat, (result, discrepancy) in enumerate(zip(Simulation,avg_Discrepancy), start=1):
#     print("Repeat:", repeat)`
#     for votingSystem, data in result.items():
#         print(votingSystem, ":", data, end="\n")
#     print()

    print('average discrepancies:', avg_Discrepancy)