import random
from math import floor


def jack_knife(ballots, percent):
    if percent >= 1 or percent <= 0:
        raise Exception("percentage needed in decimal")
    # cut dictionary keeps cut ballots
    cut = {}
    n_cut = floor(len(ballots)*percent)
    print(n_cut)
    for i in range(n_cut):
        cut = ballots.pop(random.randrange(len(ballots)))
    return ballots
