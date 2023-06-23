def condorcet(ballots, n_candidates):
    """
    Find the winner for the vote using the Condorcet Method
    :param ballots: dictionary with voters and their preference list
    :param n_candidates: number of candidates
    :return: list of winners
    """

    # when a candidate loses in comparison to any other candidate, value changes to False and is not considered anymore
    candidates = {i: True for i in range(n_candidates)}

    for i in range(n_candidates):
        if not candidates[i]:
            continue
        for j in range(i + 1, n_candidates):
            if not candidates[j]:
                continue
            i_over_j = 0
            j_over_i = 0
            for x in ballots.keys():
                for y in ballots[x]['vote']:
                    if y[0] == i:
                        i_over_j += 1
                        break
                    if y[0] == j:
                        j_over_i += 1
                        break
            if i_over_j > j_over_i:
                candidates[j] = False
            elif j_over_i > i_over_j:
                candidates[i] = False

    return [k for k, v in candidates.items() if v is True]
