import random
def dictatorship(ballots):
    dictator = random.choice(list(ballots))
    Winner = ballots[dictator]["vote"][0][0]
    return Winner
