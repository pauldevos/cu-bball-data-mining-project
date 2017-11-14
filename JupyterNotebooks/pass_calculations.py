import math


# is_open
#   determines whether a player is "open" based on distance of nearest defender
#   note that the moment that the player shoots isn't determined in this function
# Params:
#   shooter_loc: location of the shooter at a given moment as a tuple (x, y)
#   def_locs: locations of each defender as list of tuples (x, y)
# Returns:
#   tuple containing distance between shooter and closest defender and whether or not he is open, (float, bool)
def is_open(shooter_loc, def_locs):

    dists = []
    for loc in def_locs:
        dist = math.hypot(shooter_loc[0] - loc[0], shooter_loc[1] - loc[1])
        if dist < 5:
            return dist, False
        dists.append(dist)
    dists = sorted(dists)
    return dists[0], True

# pass_anticipation
#   determines the distance that the receiver travels between the beginning of the pass and the end of the pass
#   note that the moments when pass begins and ends aren't determined in this function
# Params:
#   init_receiver_loc: location of receiver at the moment the pass begins as a tuple (x, y)
#   fin_receiver_loc: location of the receiver at the moment the pass ends as a tuple (x, y)
# Returns:
#   distance that receiver travles, float
def pass_anticipation(init_receiver_loc, fin_receiver_loc):
    return math.hypot(init_receiver_loc[0] - fin_receiver_loc[0], init_receiver_loc[1] - fin_receiver_loc[1])
