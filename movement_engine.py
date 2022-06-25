
import itertools
from pprint import pprint

class movement_engine:

    def make_movement_diamond(movement):
        row_change = list(range(movement * -1, movement + 1))
        col_change = list(range(movement * -1, movement + 1))
        square = list(itertools.product(row_change, col_change))
        diamond = []
        for move in square:
            # restrict movement with no diags
            if (abs(move[0]) + abs(move[1])) <= movement:
                diamond.append(move)
        return diamond