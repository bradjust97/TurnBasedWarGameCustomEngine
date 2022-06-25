
import itertools
from pprint import pprint

# from chess_engine import game_state

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

# technically movement and row/col not needed if u query the diamond
def blocked_movement_diamond(movement, valid_moves, row_number, col_number, game_state):
    checked = [[row_number,col_number]]
    M = movement
    m = 0
    DFSList = DFS_Traverse_Diamond(checked, M, m, game_state)
    # remove dupes
    listOfLists = [list(t) for t in set(tuple(element) for element in DFSList)]
    return [tuple(l) for l in listOfLists]

def DFS_Traverse_Diamond(checked, M, m, game_state):
    newC = checked.copy()
    for square in checked:
        if(game_state.is_empty(square[0]+1, square[1]) and [square[0]+1, square[1]] not in checked):
            newC.append([square[0]+1, square[1]])

        if(game_state.is_empty(square[0], square[1]+1) and [square[0], square[1]+1] not in checked):
            newC.append([square[0], square[1]+1])
        
        if(game_state.is_empty(square[0]-1, square[1]) and [square[0]-1, square[1]] not in checked):
            newC.append([square[0]-1, square[1]])

        if(game_state.is_empty(square[0], square[1]-1) and [square[0], square[1]-1] not in checked):
            newC.append([square[0], square[1]-1])
        
    m += 1
    if(m == M):
        return newC 
    else:
        return DFS_Traverse_Diamond(newC,M,m,game_state)