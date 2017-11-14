import math


# is_open
#   determines whether a player is "open" based on distance of nearest defender
#   note that the moment that the player shoots isn't determined in this function
# Params:
#   shooter_loc: location of the shooter at a given moment as a tuple (x, y)
#   def_locs: locations of each defender as list of tuples (x, y)
def is_open(shooter_loc, def_locs):

    dists = []
    for loc in def_locs:
        dist = math.hypot(shooter_loc[0] - loc[0], shooter_loc[1] - loc[1])
        if dist < 5:
            return dist, False
        dists.append(dist)
    dists = sorted(dists)
    return dists[0], True

shooter_loc = (45.7042, 15.57870)
def_locs = [(56.27694, 25.51460), (73.64107, 25.48774), (48.6492, 35.26915), (48.46352, 14.55436), (47.51449, 24.36448)]
print(is_open(shooter_loc, def_locs))
