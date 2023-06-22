
def bordaCount(ballot_box):
    candidate_points = {}
    n_candidates = len(ballot_box[0]["vote"])

    for voter_index, rank in ballot_box.items():
        ballot = rank["vote"][:, 0]
        for position, candidate_index in enumerate(ballot):
            # first ranked candidate out of n gets n-1 points, second n-2,.., last gets 0
            points = n_candidates - position - 1
            if candidate_index not in candidate_points:
                candidate_points[candidate_index] = 0
            candidate_points[candidate_index] += points

    # if output list & not dic
    #candidate_points_list = list(candidate_points.items())
    #candidate_points_list = sorted(candidate_points_list, key=lambda x: x[1], reverse=True)
    # sorted_candidate_indices = [candidate_index for candidate_index, _ in candidate_points_list]
    return candidate_points
