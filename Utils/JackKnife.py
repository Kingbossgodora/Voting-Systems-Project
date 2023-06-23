import random
from math import floor
def JackKnife(ballots, percent):
    if(percent >= 1 or percent <= 0):
        raise exception("percentage needed in decimal")
    #cut dictionary keeps cut ballots
    cut={}
    n_cut= floor(len(ballots)*percent)
    print(n_cut)
    for i in range(n_cut):
        cut=ballots.pop(random.randrange(len(ballots)))
    return ballots
