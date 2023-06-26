import numpy


def discrepancy(votingSystem, ballotBox, idealCandidate, candidates, n_candidates):
    winners = votingSystem(ballotBox, n_candidates)
    winner = list(winners.keys())[0]

    candidate_coords = candidates[winner]
    dist = numpy.sqrt((idealCandidate[0] - candidate_coords[0]) ** 2 + (idealCandidate[1] - candidate_coords[1]) ** 2)
    return dist
