def plurality(ballots, *args):
    candidate_points = {}
    
    for i in range(len(ballots)):        
        #fill the candidate dictionary and count the number of first choice
        vote=ballots[i]["vote"][:, 0][0]
        if vote not in candidate_points:
            candidate_points[vote]=0
        candidate_points[vote] +=1
    
  #returns a dictionary with single vote results
  #return candidate_points
    

    Winner = max(zip(candidate_points.values(), candidate_points.keys()))[1]
    Wvote = max(zip(candidate_points.values(), candidate_points.keys()))[0]

    nw=0
    for x in candidate_points.values():
        if x >= Wvote:
            nw+=1
        if nw > 1:
            print("There is a tie")
            return
    return Winner
