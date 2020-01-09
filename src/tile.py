# A Tile is one of the following
t0       = "blue"
t1       = "yellow"
t2       = "red"
t3       = "black"
t4       = "lightblue"
one_tile = "T"

tiles    = [t0, t1, t2, t3, t4]

def idx_to_tile(i):
    return tiles[i]

def tile_to_idx(t):
    if (t0 == t):
        return 0
    elif (t1 == t):
        return 1
    elif (t2 == t):
        return 2
    elif (t3 == t):
        return 3
    elif (t4 == t):
        return 4
    elif (one_tile == t):
        return 6 
    else:
        raise ValueError()

def tile_comp(t0, t1):
    if (t0 == one_tile):
        return 1 
    elif (t1 == one_tile):
        return -1
    else:
        return -1 if tiles.index(t0) < tiles.index(t1) else 0 if tiles.index(t0) == tiles.index(t1) else 1

################################
# Printing Utilities           #
################################

# ansi color codes (foreground colors)
f_blu = "\x1B[34m"
f_yel = "\x1B[33m" 
f_red = "\x1B[31m"
f_gry = "\x1B[32m"
f_mag = "\x1B[35m"
f_grn = "\x1B[36m"
norm  = "\x1B[0m"

colors    = [f_blu, f_yel, f_red, f_gry, f_mag]

color_map = {tiles[i]: colors[i] for i in range(len(tiles))}

def tile_to_color(t):
    return color_map[t]

# foreground -> background
def f_to_b(s):
    return s.replace("3", "4", 1)

tile_map = {tiles[i]: color_map[tiles[i]] + str(i) + norm for i in range(len(tiles))}
tile_map[one_tile] = f_grn + one_tile + norm

def tile_to_str(t):
    return tile_map[t]