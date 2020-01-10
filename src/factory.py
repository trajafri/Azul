import random
from tile import *

# number of tiles per factory
F_SIZE = 4

def make_bag():
    ls = [t0] * 20 + [t1] * 20 + [t2] * 20 + [t3] * 20 + [t4] * 20
    random.shuffle(ls)
    return ls

def necessary_factories(players):
    return 2 * (players - 2) + 5

def split_by(ls, n):
    if len(ls) == 0:
        return []
    elif len(ls) < n:
        return [ls]
    else:
        rec = split_by(ls[n:], n)
        rec.insert(0, ls[:n])
        return rec

class FactorySet(object):
    def __init__(self, middle, factories):
        self.middle    = middle
        self.factories = factories
    
def restock(bag, n):
    bag_cp = [b for b in bag]
    random.shuffle(bag_cp)
    shuffled_bag = bag_cp
    tiles        = shuffled_bag[:F_SIZE * n]
    new_bag      = shuffled_bag[F_SIZE * n - 1:]
    factories    = split_by(tiles, F_SIZE)
    return new_bag, FactorySet([one_tile], factories)

def partition_by(pred, ls):
    ans = []
    other = []
    for t in ls:
        if pred(t):
            list.append(ans, t)
        else:
            list.append(other, t)
    return ans, other

def partition_factory(tile, f):
    return partition_by(lambda x: x == tile or x == one_tile, f)

def pull_from_factory(i, tile, fact_set):
    if i < 0:
        same, diff = partition_factory(tile, fact_set.middle)
        return same, FactorySet(diff, fact_set.factories) 
    else:
        desired_factory = fact_set.factories[i]
        same, diff = partition_factory(tile, desired_factory)
        return same, FactorySet(diff + fact_set.middle, 
                                [[] if j == i else fact_set.factories[j] 
                                 for j in range(len(fact_set.factories))])

################################
# Printing Utilities           #
################################

def fact_to_los(f, i):
    label = "f-" + str(i) + (" " * F_SIZE)
    tiles = ""
    for t in f:
        tiles = tiles + tile_to_str(t)
    return ["|" + label, "|  " + (" " * (F_SIZE - len(f))) + tiles + " "]

def mid_to_los(m):
    label = "middle" + (" " * max(0, len(m) - 4))
    tiles = ""
    for t in m:
        tiles = tiles + tile_to_str(t)
    return ["|" + label, "|  " + tiles]