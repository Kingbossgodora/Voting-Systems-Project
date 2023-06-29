import random


def dictatorship(ballots, *args):
    dictator = min(ballots.keys())
    Winner = ballots[dictator]["vote"][0][0]
    Winner_dic = {Winner: True}
    return Winner_dic
