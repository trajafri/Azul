from tile      import *
from factory   import *
from functools import reduce

def place_move_wall(p, w):
    (x, y) = p
    return [w[i] if i != x else [w[i][j] if j != y else (w[x][y][0], True) for j in range(len(w[0]))]
            for i in range(len(w))]

def count_points(p, w):
    (x, y)    = p
    top_vec   = 0
    for i in range(y-1, -1, -1):
        if not w[x][i][1]:
            break
        top_vec += 1
    bot_vec   = 0
    for i in range(y+1, len(w)):
        if not w[x][i][1]:
            break
        bot_vec += 1
    left_vec  = 0
    for i in range(x-1, -1, -1):
        if not w[i][y][1]:
            break
        left_vec += 1
    right_vec = 0
    for i in range(x+1, len(w)):
        if not w[i][y][1]:
            break
        right_vec += 1
    vert_count = top_vec + bot_vec
    hori_count = left_vec + right_vec
    return 1 +  vert_count + hori_count + (0 if (hori_count * vert_count == 0) else 1)

def is_stageline_ready(sgl):
    (n, d) = sgl
    if not d:
        return False
    else:
        (c, t) = d
        return t if n == c else False

def overflow_error(n):
    return sum(Board.OFLOW[:n])

def place_and_score_staging(score, staging, wall):
    return help_score_staging(0, score, staging, wall)

def get_tile_spot(i, t, w):
    for j in range(len(w[0])):
        if w[i][j][0] == t:
            return (i, j)
    raise Exception("get_tile_spot")

def help_score_staging(i, score, stage, w):
    if i < 0 or i > 5:
        raise Exception("help_score_staging")
    if i == 5:
        return (score, w)
    elif is_stageline_ready(stage[i]):
        staged_tile    = is_stageline_ready(stage[i])
        tile_goes_here = get_tile_spot(i, staged_tile, w)
        tile_points    = count_points(tile_goes_here, w)
        return help_score_staging(i + 1, tile_points + score, stage, place_move_wall(tile_goes_here, w))
    else:
        return help_score_staging(i + 1, score, stage, w)

def add_tiles_to_line(amt, tile, line):
    capacity       = line[0]
    reasonable_amt = min(amt, capacity)
    if not line[1]:
        return (line[0], (reasonable_amt, tile))
    else:
        idx = line[0]
        (k, tile2) = line[1]
        if tile != tile2:
            raise Exception("add_tiles_to_line")
        k_cap = idx - k
        new_k = k + min(reasonable_amt, k_cap)
        return (idx, (new_k, tile))

def update_one_tile(one_tile, is_one_tile):
    return one_tile or (is_one_tile and True)

class Board(object):

    # Initial wall and staging area

    WALL = [[(t0, False), (t1, False), (t2, False), (t3, False), (t4, False)]
           ,[(t4, False), (t0, False), (t1, False), (t2, False), (t3, False)]
           ,[(t3, False), (t4, False), (t0, False), (t1, False), (t2, False)]
           ,[(t2, False), (t3, False), (t4, False), (t0, False), (t1, False)]
           ,[(t1, False), (t2, False), (t3, False), (t4, False), (t0, False)]]

    SG_AR = [(1, False), (2, False), (3, False), (4, False), (5, False)]

    OFLOW = [-1, -1, -2, -2, -2, -3, -3]

    def __init__(self, score, wall, staging, error_count, one_tile):
        self.score = score
        self.wall = wall
        self.staging = staging
        self.error_count = error_count
        self.one_tile = one_tile

    def put_staging(self, staging): 
        return Board(self.score, self.wall, staging, self.error_count, self.one_tile)

    def put_wall(self, wall): 
        return Board(self.score, wall, self.staging, self.error_count, self.one_tile)

    def place_move(self, posn):
        return Board(self.score, 
                     place_move_wall(posn, self.wall),
                     self.staging,
                     self.error_count,
                     self.one_tile)

    def reset_lines(self):
        return Board(self.score,
                     self.wall,
                     [(max_c, False if (not s or (max_c <= s[0])) else s)
                      for (max_c, s) in self.staging],
                     self.error_count,
                     self.one_tile)

    def update_score(self):
        reduced_score     = overflow_error(self.error_count) + self.score
        net_pts, new_wall = place_and_score_staging(reduced_score, self.staging, self.wall) 
        score = max(0, net_pts)
        return Board(score, new_wall, self.staging, 0, False).reset_lines()

    def wipe_turn(self, tiles, factoryset, is_one_tile):
        amt_tiles = len(tiles)
        new_extra = min(self.error_count + (1 + amt_tiles if is_one_tile else amt_tiles), len(self.OFLOW))
        return (Board(self.score, self.wall, self.staging, new_extra, update_one_tile(self.one_tile, is_one_tile))
                , factoryset)

    def add_tiles(self, fset, f, i, tile):
        to_overflow = i > 5 or i < 0
        tiles, new_fset = pull_from_factory(f, tile, fset)
        is_one_tile = one_tile in tiles
        if to_overflow:
            return self.wipe_turn(tiles, new_fset, is_one_tile)
        else:
            amount_to_add  = (len(tiles) - 1) if is_one_tile else len(tiles)
            current_amount = self.staging[i - 1][1][0] if not to_overflow and self.staging[i - 1][1] else 0 
            leftover       = max(amount_to_add - (i - current_amount), 0)
            new_extra      = min(leftover + (1 + self.error_count if is_one_tile else self.error_count), len(self.OFLOW))
            new_stage      = [add_tiles_to_line(amount_to_add, tile, (a, d)) if (a == i) else (a, d) for (a, d) in self.staging]
            return (Board(self.score, self.wall, new_stage, new_extra, update_one_tile(self.one_tile, is_one_tile))
                    , new_fset)

    def contains_full_row(self):
        return len(self.wall[0]) == max([[d for (a, d) in r].count(True) for r in self.wall])

    def num_full_rows(self):
        wall_width = len(self.wall[0])
        return [(wall_width == [d for (a, d) in r].count(True)) for r in self.wall].count(True)

    def calculate_bonus(self):
        flat_wall       = [item for l in self.wall for item in l]
        transpose       = lambda l: [[l[i][j] for i in range(len(l[0]))] for j in range(len(l))]
        count_full_rows = lambda l: [all([d for (a, d) in r]) for r in l].count(True)
        horizontals     = count_full_rows(self.wall)
        verticals       = count_full_rows(transpose(self.wall))

        t_counts        = [0] * len(tiles)
        for (t, d) in flat_wall:
            if d:
                t_counts[tile_to_idx(t)] += 1 

        fives           = t_counts.count(5)

        return (fives * 10) + (horizontals * 2) + (verticals * 7)

    def bonusify_board(self):
        return Board(self.score + self.calculate_bonus(), self.wall, self.staging, self.error_count, self.one_tile)


    ################################
    # Printing Utilities           #
    ################################

    def board_to_los(self, p):
        # If you want to change what a default wall looks like, you just have to understand the line below
        w_line_to_str = lambda l: [" " + tile_to_str(a) + " " if d else f_to_b(tile_to_color(a)) + "[*]" + norm
                                   for (a, d) in l]
        board_rows    = [(str(i), sg_line_to_str(self.staging[i]), w_line_to_str(self.wall[i]))
                         for i in range(len(self.wall))]
        largest_line  = max([a for (a, d) in self.staging])
        player_str    = "Player #" + str(p + 1)
        sep           = "+" + ("-" * len(player_str)) + "+ "
        sep_pad       = 18 #only thing hard coded in this printing
        separator     = sep + (" " * sep_pad)
        score_str     = "score: " + str(self.score)
        overflow_str  = "#over: " + str(self.error_count) + str(" *" if self.one_tile else "")
        board_strs    = [row_to_str(x, largest_line) for x in board_rows]
        board_str_len = len(board_strs[0])
        score_string  = sep + score_str
        score_pad     = len(separator) - len(score_string)
        player_string = player_str + " | " + overflow_str
        player_pad    = len(separator) - len(player_string)
        return ([score_string + (" " * score_pad), player_string + (" " * player_pad), separator]
                + board_strs)

def sg_line_to_str(p):
    (max_c, s)   = p
    empty_char   = "."
    char         = tile_to_str(s[1]) if s else empty_char
    occ_slots    = s[0] if s else 0
    filled_slots = [char] * occ_slots
    rest_slots   = [empty_char] * (max_c - occ_slots)
    return rest_slots + filled_slots

def row_to_str(a, ln):
    (i, l, w) = a
    padding   = [" "] * (ln - len(l))

    l_str     = ""
    for x in (padding + l):
        l_str = l_str + x + " "

    w_str     = ""
    for x in w:
        w_str = w_str + x

    return i + "| " + l_str + " |" + w_str

def boards_to_str(bs):
    parted_boards    = split_by([(bs[i], i) for i in range(len(bs))], 2)
    board_str_sample = bs[0].board_to_los(0)
    board_pad        = 10 * " "

    result = ""
    for boards in parted_boards:
        b_res = [""] * len(board_str_sample)
        for bo in boards:
            (b, i) = bo
            xs     = b.board_to_los(i)
            b_res  = [b_res[i] + xs[i] + board_pad for i in range(len(b_res))]
        b_res = [s + "\n" for s in b_res]
        for s in b_res:
            result = result + s
        result += "\n"
    return result

#print(boards_to_str([Board(12, Board.WALL, Board.SG_AR, 0, False).place_move((0, 2)).place_move((4, 4)),
#Board(12, Board.WALL, Board.SG_AR, 0, False).place_move((0, 2)).place_move((4, 3)),
#Board(12, Board.WALL, Board.SG_AR, 0, False).add_tiles(FactorySet([t0,t0,t0,t1,t1,t3],[]), -1, 2, t0)[0]
#]))

