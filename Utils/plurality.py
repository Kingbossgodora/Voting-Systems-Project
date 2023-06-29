def plurality(ballots, *args):
    candidate_points = {}
    
    for i in range(len(ballots)):
        try:
            #fill the candidate dictionary and count the number of first choice
            vote=ballots[i]["vote"][:, 0][0]
            if vote not in candidate_points:
                candidate_points[vote]=0
            candidate_points[vote] +=1
        except:
            continue
  
    #returns a dictionary with single vote results
    
    Wvote = max(zip(candidate_points.values(), candidate_points.keys()))[0]
    ordered_candidate_point = dict(sorted(candidate_points.items(), key=lambda x:x[1], reverse=True))
    nw=0
    for x in candidate_points.values():
        if x >= Wvote:
            nw+=1
        if nw > 1:
            print("There is a tie")
            return ordered_candidate_point
    
    return ordered_candidate_point
