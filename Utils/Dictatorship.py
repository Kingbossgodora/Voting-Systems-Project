import random
def dictatorship(ballots, *args):
    dictator = random.choice(list(ballots))
    Winner = ballots[dictator]["vote"][0][0]
    Winner_dic = {Winner: True}
    return Winner_dic
