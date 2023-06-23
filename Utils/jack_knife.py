import random
from math import floor
def JackKnife(ballots, percent):
    if(percent >= 1 or percent <= 0):
        raise exception("percentage needed in decimal")
    #cut dictionary
    n_cut= floor(len(ballots)*percent)
    
    for key in random.sample(ballots.keys(), n_cut):
        del ballots[key]
    return ballots
