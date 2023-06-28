from math import floor


def scoring(ballots, n_candidates):
    """
    Find a score that each candidate gets in a scoring voting.
    :param ballots: dictionary with voters and their preference list
    :param n_candidates: number of candidates
    :return: dictionary of candidates and their respective score
    """

    max = 0
    candidates = {}
    n_values = 10

    for i in range(n_candidates):
        candidates[i] = 0

    # find maximum distance in the graph to calculate the value of 1 point in scoring
    for i in ballots.keys():
        for x in ballots[i]['vote']:
                if x[1] > max:
                    max = x[1]

    value = n_values / max

    for i in ballots.keys():
        for x in ballots[i]['vote']:
                candidates[x[0]] += floor(n_values - x[1] * value)
    
    #return ordered candidates
    ordered_candidate_point = dict(sorted(candidates.items(), key=lambda x:x[1], reverse=True))
    return ordered_candidate_point
