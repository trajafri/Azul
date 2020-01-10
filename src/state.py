from board   import *
from tile    import *
from factory import *
import functools


class State(object):
    def __init__(self, np, ps, bs, t, fset, nf, bag):
        self.np   = np
        self.ps   = ps
        self.bs   = bs 
        self.t    = t 
        self.fset = fset 
        self.nf   = nf
        self.bag  = bag 

    def is_last_round(self):
        return any([b.contains_full_row() for b in self.bs])

    def is_round_end(self):
        return all([len(f) == 0 for f in self.fset.factories + self.fset.middle])

    def next_turn(self):
        return (self.t + 1) % self.np

    def play_move(self, move):
        (move_factory_idx, move_tile, move_line_num) = move
        new_board, new_factory_set = self.bs[self.t].add_tiles(self.fset, move_factory_idx - 1, move_line_num + 1, move_tile)
        return State(self.np,
                     self.ps,
                     [new_board if i == self.t else self.bs[i] for i in range(len(self.bs))],
                     self.next_turn(),
                     new_factory_set,
                     self.nf,
                     self.bag)
    
    def end_info(self):
        new_boards = [b.bonusify_board() for b in self.bs]
        def compare_board(l, r):
            if l.score == r.score:
                if l.num_full_rows() == r.num_full_rows():
                    return 0
                elif l.num_full_rows() > r.num_full_rows():
                    return -1
                else:
                    return 1
            elif l.score > r.score:
                return -1
            else:
                return 1
        
        sort_fun       = lambda l, r: compare_board(l, r) == -1
        ranked_boards  = sorted(new_boards, key=functools.cmp_to_key(sort_fun))
        winning_boards = [b for b in ranked_boards if compare_board(b, ranked_boards[0]) == 0]
        return ([b.score for b in new_boards],
                [new_boards.index(b) for b in winning_boards],
                new_boards,
                ranked_boards)
        
    ################################
    # Printing Utilities           #
    ################################

    def state_to_str(self):
        factories       = self.fset.factories
        mid             = sorted(self.fset.middle, key=functools.cmp_to_key(tile_comp))
        parted_facts    = split_by([(factories[i], i + 1) for i in range(len(factories))], 5)
        fact_str_sample = fact_to_los([t0, t0, t0, t0], 0)
        fact_sep        = len(fact_str_sample[0]) * "+"
        factories_sep   = (fact_sep * 5) + "\n"
        fact_str        = ""
        for facts in parted_facts:
            f_res = [""] * len(fact_str_sample)
            for f in facts:
                (fact, i) = f
                sf = fact_to_los(fact, i)
                f_res = [f_res[i] + sf[i] for i in range(len(f_res))]
            f_res = [s + "\n" for s in f_res]
            for s in f_res:
                fact_str = fact_str + s
            fact_str += "\n"
        parted_boards    = split_by([(self.bs[i], i + 1) for i in range(self.np)], 2)
        board_str        = boards_to_str(self.bs)
        mid_str         = ""
        for x in mid_to_los(mid):
            mid_str = mid_str + x + "\n"
        return factories_sep + fact_str + mid_str + "\n" + board_str

#print(State(4, 
#            [], 
#            [Board(0, Board.WALL, Board.SG_AR, 0, False)] * 4, 
#            0,
#            restock(make_bag(), necessary_factories(4))[1],
#            necessary_factories(4),
#            []).state_to_str())