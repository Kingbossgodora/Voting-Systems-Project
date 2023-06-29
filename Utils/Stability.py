from Utils.jack_knife import JackKnife

def stability(ballots, function, tries, percent, n_candidates, *args):
    candidate_point = {}
    
    if(percent >= 1 or percent <= 0):
        raise Exception("percentage needed in decimal")

    #run Jackknife function specifies amount of times
    for i in range(tries):
        
        w = function(JackKnife(ballots, percent), n_candidates)
        winner = list(w.keys())[0]
        if winner not in candidate_point:
            candidate_point[winner]=0
        candidate_point[winner] +=1
    
    #changes score to percentage
    for keys in candidate_point:
        candidate_point[keys]= round((candidate_point[keys]/tries), 2)
    ordered_candidate_point = dict(sorted(candidate_point.items(), key=lambda x:x[1], reverse=True))
    
    #returns dic of candidates and percentage of victory
    return ordered_candidate_point
