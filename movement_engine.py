
import itertools
from pprint import pprint
from tabnanny import check
from typing import List

from terrain.Terrain import Terrain

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
def blocked_movement_diamond(movement, row_number, col_number, game_state):
    checked = [[row_number,col_number]]
    M = movement
    m = 0

    Listy = BFS_Traverse_Diamond(checked, M, m, game_state)
    # Listy = DFS_Traverse_Diamond(checked, [row_number,col_number], M, m, game_state)
    
    # remove dupes
    listOfLists = [list(t) for t in set(tuple(element) for element in Listy)]
    # turn list of list to list of tuples
    diamond = [tuple(l) for l in listOfLists]
    terrainDiamond = runDijkstraAlgorithmAndFilterMovement(game_state, M, [row_number,col_number], diamond)
    terrainDiamondListTuples = [tuple(l) for l in terrainDiamond]
    return terrainDiamondListTuples

def BFS_Traverse_Diamond(checked, M, m, game_state):
    newC = checked.copy()
    for square in checked:
        # check to right
        if(game_state.is_empty(square[0]+1, square[1]) and [square[0]+1, square[1]] not in checked):
            newC.append([square[0]+1, square[1]])

        # check below
        if(game_state.is_empty(square[0], square[1]+1) and [square[0], square[1]+1] not in checked):
            newC.append([square[0], square[1]+1])
        
        # check left
        if(game_state.is_empty(square[0]-1, square[1]) and [square[0]-1, square[1]] not in checked):
            newC.append([square[0]-1, square[1]])

        # check above
        if(game_state.is_empty(square[0], square[1]-1) and [square[0], square[1]-1] not in checked):
            newC.append([square[0], square[1]-1])
        
    m += 1
    if(m == M):
        return newC
    else:
        return BFS_Traverse_Diamond(newC,M,m,game_state)
# TODO make a dfs instead. this is bc we have terrain 

# THIS DOESNT WORK
def DFS_Traverse_Diamond(checked, square, M, m, game_state):
    newC = checked.copy()
    for neighbor in game_state.getTerrainNeighbors(square[0], square[1]): # GTN should return a list of terrains given a [x,y]
        neighborXY = [neighbor.getRow(), neighbor.getCol()]
        if neighborXY not in checked:
            newm = m + neighbor.getMovementPenalty() + 1
            if newm < M:
                newC.append(neighborXY) # Dont append a terrain type here, append the [x,y] of the neighbor terrain
                DFS_Traverse_Diamond(newC, neighborXY, M, newm, game_state) # THIS IS RETURNING< BREAKING THE ABILITY TO CHECK NEIGHBORS 
            elif newm == M:
                newC.append(neighborXY)
    
    # DONT THINK THIS IS GONNA WORK. WHAT HAPPENS IF YOU GO AROUND AND FIND A TILE ALREADY CHECKED? ACCORDING TO THIS IT WILL IGNORE ANY CHECKED TILE
    #DJ ALG WILL RETURN SHORTEST PATH TO EACH NODE. JUST USE THE MOVEMENT PENALTY AS THE COST TO GET TO IT FROM CURRENT NODE
    
    return newC


def getUnvisitedWithSmallestDistance(d, visited):
    # returns a tuple (x,y) of the point that is closet to start which hasnt been checked 
    leastDistanceFromStart = 999999
    unvisitedWithSmallestDistance = None
    for vertex, value in d.items():
        if vertex not in visited:
            if value[0] <= leastDistanceFromStart:
                leastDistanceFromStart = value[0]
                unvisitedWithSmallestDistance = vertex
    return unvisitedWithSmallestDistance


def dijkstraAlgorithm(game_state, startingSquare, possibleSquares):
    # possible squares is a list of lists, but need to change that to list of tuples in form [(x,y),...]
    possibleSquaresTuples = [tuple(l) for l in possibleSquares]
    # starting square is a list, change to tuple of form (x,y)
    startingSquareTuple = tuple(startingSquare)
    distanceDictionary = {} # point name (x,y) -> (shortestDistanceFromStart, (x,y))
                            # vertex -> (shortestDistanceFromStart, prevVertex)
    visitedPoints = [] # list of tuples we have already visited
    for square in possibleSquaresTuples:
        distanceDictionary[square] = (999999, None)
    distanceDictionary[startingSquareTuple] = (0, None)

    while(len(visitedPoints) < len(possibleSquaresTuples)):
        currentVertex = getUnvisitedWithSmallestDistance(distanceDictionary, visitedPoints)
        distanceToStart = distanceDictionary[currentVertex][0]
        terrainNeighbors = game_state.getTerrainNeighbors(currentVertex[0], currentVertex[1])
        # print(terrainNeighbors)
        for tn in terrainNeighbors:
            tnXY = (tn.getRow(), tn.getCol())
            if(tnXY in possibleSquaresTuples):
                distanceFromCurrentVertex = tn.getMovementPenalty() + 1
                totalDistanceToStart = distanceFromCurrentVertex + distanceToStart
                if(distanceDictionary[tnXY][0] > totalDistanceToStart):
                    distanceDictionary[tnXY] = (totalDistanceToStart, currentVertex)
        visitedPoints.append(currentVertex)
    return distanceDictionary

def runDijkstraAlgorithmAndFilterMovement(game_state, M, startingSquare, possibleSquares):
    # return list of 2x1 lists [[x,y], [x,y]...]
    movementSquares = []
    distanceDictionary = dijkstraAlgorithm(game_state, startingSquare, possibleSquares)
    for point, value in distanceDictionary.items():
        if value[0] <= M:
            movementSquares.append(list(point))
    return movementSquares