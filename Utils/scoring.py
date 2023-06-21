import numpy as np
from math import floor


def scoring(ballots, n_candidates):

    max = 0
    candidates = {}
    n_values = 10

    for i in range(n_candidates):
        candidates[i] = 0

    for i in ballots.keys():
        for x in ballots[i]['vote']:
                if x[1] > max:
                    max = x[1]

    value = n_values / max

    for i in ballots.keys():
        for x in ballots[i]['vote']:
                candidates[x[0]] += floor(n_values - x[1] * value)

    return candidates
