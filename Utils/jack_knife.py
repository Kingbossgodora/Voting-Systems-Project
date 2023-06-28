import random
from math import floor

def JackKnife(ballots, percent):
    temp_ballot = dict(ballots)
    if(percent >= 1 or percent <= 0):
        raise exception("percentage needed in decimal")
    
    #cut dictionary
    n_cut= floor(len(ballots)*percent)
    for key in random.sample(temp_ballot.keys(), n_cut):
        del temp_ballot[key]
    
    return ballots
