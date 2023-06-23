from math import floor

def IRV(ballots):
    candidate_points = {}
    losers = []
    majority = floor(len(ballots)/2)
    #print("majority:", majority)
    Wvote = 0
    
    #loop until a candidate wins absolute majority
    while(Wvote<= majority):
        candidate_points.clear()
        for i in range(len(ballots)):
            vote=ballot_box[i]["vote"][:, 0][0]
            #skips eliminated candidates and select vote for next one --- need work
            c=0
            while(vote in losers):
                vote=ballot_box[i]["vote"][:, 0][c]
                c+=1
            if vote not in candidate_points:
                candidate_points[vote]=0
            candidate_points[vote] +=1
            
        #add the least prefered candidate to the eliminated list
        loser = min(zip(candidate_points.values(), candidate_points.keys()))[1]
        #print("loser", loser)
        #print(candidate_points)
        losers.append(loser)
        Wvote = max(zip(candidate_points.values(), candidate_points.keys()))[0]
    
    return candidate_points 
    
    #return max(zip(candidate_points.values(), candidate_points.keys()))[1]
