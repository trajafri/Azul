from tile    import *
from factory import *
from board   import *
from state   import *

def manual_player(st, b):
    print(st.state_to_str() + "\n")
    print(f"You are player {st.t + 1} ")
    print("Input m represents the middle factory, a line number out of range goes in overflow.")
    inp       = raw_input("Input format (factory-number tile-number line-number)\n: ")
    maybe_err = validate_input(st, b, parse_input(inp))
    while(isinstance(maybe_err, str)):
        maybe_err = validate_input(st, b, parse_input(input()))
    return maybe_err

def parse_input(inp):
    pinp = inp.split()
    if len(pinp) == 3:
        pfid  = pinp[0] if pinp[0] == "m" or not pinp[0].isnumeric() else int(pinp[0])
        ptile = pinp[1] if not pinp[1].isnumeric() else int(pinp[1])
        pline = pinp[2] if not pinp[2].isnumeric() else int(pinp[2])
        return (pfid, ptile, pline)
    else: return pinp

def validate_input(st, b, i):
    if len(i) != 3:
        return f"Expected at least 3 inputs, given {len(i)}"
    else:
        (f_id, tile, stg_lin_num) = i
        if not is_valid_f_id(f_id, necessary_factories(st.np)):
            return make_bad_f_id_str(f_id)
        elif not is_valid_tile(tile):
            return make_bad_tile_str(tile)
        elif not is_valid_line_num(stg_lin_num):
            return make_bad_line_str(tile)
        elif invalid_factory_move(idx_to_tile(tile), f_id, st.fset):
            return invalid_factory_move(idx_to_tile(tile), f_id, st.fset)
        elif invalid_tile_move(idx_to_tile(tile), stg_lin_num, b):
            return invalid_tile_move(idx_to_tile(tile), stg_lin_num, b)
        else:
            return sanitize(f_id, tile, stg_lin_num)

def sanitize(f_id, tile, line_num):
    return (clean_f_id(f_id), idx_to_tile(tile), clean_stg_line(line_num))

################################
# Validation Utilities         #
################################

def is_valid_f_id(f_id, num_factories):
    return f_id == "m" or (isinstance(f_id, numbers.Number) and x > 0 and x <= num_factories)

def is_valid_tile(t):
    return isinstance(t, numbers.Number) and t < len(tiles)

def is_valid_lin_num(n):
    return isinstance(n, numbers.Number)

def invalid_factory_move(tile, f_id, fset):
    factory_in_question = fset.middle if f_id == "m" else fset.factories[f_id - 1]
    if len(factory_in_question) == 0:
        return "can't ask for tiles from empty factory"
    elif factory_in_question[0] == one_tile and len(factory_in_question) == 1:
        return "can't only take the one_tile"
    elif not (tile in factory_in_question):
        return "can't take a color not in the chosen factory"
    else:
        return False

def invalid_tile_move(tile, stg_lin_num, b):
    if stg_lin_num >= len(b.staging):
        return False
    else:
        stg_line      = b.staging[stg_lin_num]
        is_valid_line = not stg_line[0] or stg_line[1][1] == tile
        if not is_valid_line:
            return "can't place a tile on a line that contains a different colored tile"
        elif any([p[0] == tile and p[1] for p in b.wall[stg_lin_num]]):
            return "can't place a tile on the same row as the wall where the tile is already placed"
        else: return False

def clean_f_id(f_id):
    if f_id == "m":
        return -1
    else:
        return f_id

def clean_stg_line(s_line):
    if s_line < 0 or s_line > 4:
        return 6
    else:
        return s_line

def make_bad_tile_str(x):
    return f"oops! expected tile to be one of the listed numbers, got: {x}"

def make_bad_line_str(x):
    return f"oops! expected line number to be between [0,4] or 6, got: {x}"

def make_bad_f_id_str(x):
    return f"oops! expected either \"m\" or a number between 1 and 5; got: {x}"