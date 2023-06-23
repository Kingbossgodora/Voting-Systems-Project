from math import floor


def instant_runoff(ballots):
    candidate_points = {}
    losers = []
    majority = floor(len(ballots) / 2)
    wvote = 0

    # loop until a candidate wins absolute majority
    while wvote <= majority:
        candidate_points.clear()
        for i in ballots.keys():
            vote = ballots[i]["vote"][:, 0][0]
            # skips eliminated candidates and select vote for next one
            c = 0
            while vote in losers:
                vote = ballots[i]["vote"][:, 0][c]
                c += 1
            if vote not in candidate_points:
                candidate_points[vote] = 0
            candidate_points[vote] += 1

        # add the least preferred candidate to the eliminated list
        loser = min(zip(candidate_points.values(), candidate_points.keys()))[1]
        losers.append(loser)
        wvote = max(zip(candidate_points.values(), candidate_points.keys()))[0]

    return candidate_points

    # return max(zip(candidate_points.values(), candidate_points.keys()))[1]
