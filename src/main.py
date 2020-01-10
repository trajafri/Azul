from board   import *
from factory import *
from player  import *
from tile    import *
from state   import *
import random

# This can be improved a lot. This is ported as is and we didn't care a lot about the
# interface since we were more concerned about the AI side instead of the interface side.

NUM_P = 2

def game_state():
    start_bag     = make_bag()
    num_players   = NUM_P
    players       = [manual_player] * num_players
    boards        = [Board(0, Board.WALL, Board.SG_AR, 0, False)] * num_players
    num_factories = necessary_factories(num_players)
    the_bag, fset = restock(start_bag, num_factories)
    return State(num_players, players, boards, random.randint(0, num_players-1), fset, num_factories, the_bag)

def clean_up(st, gn = False):
    next_t     = [i for i in range(len(st.bs)) if st.bs[i].one_tile][0]
    the_bag, fset = restock(st.bag, st.nf)
    new_boards    = [b.update_score() for b in st.bs]
    new_state     = State(st.np,
                          st.ps,
                          new_boards,
                          next_t,
                          fset,
                          st.nf,
                          make_bag())
    return next_state(new_state, gn)

def make_a_move(st, gn = False):
    current_player = st.ps[st.t]
    current_board  = st.bs[st.t]
    player_move    = current_player(st, current_board)
    new_state      = st.play_move(player_move)
    return next_state(new_state, gn)

def end_game(st, gn = False):
    _, winners, new_boards, ranked_boards = st.end_info()
    f_winners = [1 + w for w in winners]
    if gn:
        print(f"game {gn} winners: {f_winners}")
        return f_winners
    else:
        print("GAME OVER")
        print("Final Boards")
        print(boards_to_str(st.bs))
        print("Winner(s): ", end="")
        print(str(f_winners) + "\n")
        i = 1
        for b in ranked_boards:
            print(f"{i}. Player {new_boards.index(b) + 1}\t{b.score}")

def next_state(st, gn = False):
    if st.is_last_round():
        return end_game(st, gn)
    elif st.is_round_end():
        return clean_up(st, gn)
    else:
        return make_a_move(st, gn)

def go():
    return next_state(game_state())

go()