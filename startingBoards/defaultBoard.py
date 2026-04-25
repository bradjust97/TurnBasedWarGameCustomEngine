import random

from enums import Player, SquareBoard, TerrainEnums
from terrain.Building import Building
from terrain.Terrain import Terrain
from units.Archer import Archer
from units.Catapult import Catapult
from units.Footman import Footman
from units.King import King
from units.Knight import Knight
from units.ScoutCavalry import ScoutCavalry


# One of each playable type per side, stacked on the south road band.
# White on row 13, buffer row 14, black on row 15, cols 5..10.
WHITE_ROW = 13
BLACK_ROW = 15
START_COL = 5

_piece_factories = [Footman, Archer, ScoutCavalry, Catapult, King]

white_pieces = [cls(WHITE_ROW, START_COL + i, Player.PLAYER_1) for i, cls in enumerate(_piece_factories)]
black_pieces = [cls(BLACK_ROW, START_COL + i, Player.PLAYER_2) for i, cls in enumerate(_piece_factories)]


board = [[Player.EMPTY for _ in range(SquareBoard.DIMENSIONS)] for _ in range(SquareBoard.DIMENSIONS)]

for piece in white_pieces:
    board[piece.get_row_number()][piece.get_col_number()] = piece
for piece in black_pieces:
    board[piece.get_row_number()][piece.get_col_number()] = piece


terrainMap = [
    [Terrain(TerrainEnums.ROAD.NAME, y, x, TerrainEnums.ROAD.DEFENSEBONUS, TerrainEnums.ROAD.MOVEMENTPENALTY)
     for x in range(SquareBoard.DIMENSIONS)]
    for y in range(SquareBoard.DIMENSIONS)
]

possibleTerrains = [TerrainEnums.PLAINS, TerrainEnums.FOREST, TerrainEnums.PLAINS, TerrainEnums.FOREST, TerrainEnums.MOUNTAIN]

for i in range(SquareBoard.DIMENSIONS):
    for j in range(SquareBoard.DIMENSIONS):
        if i > 2 and i < SquareBoard.DIMENSIONS - 3:
            choiceTerrainEnums = random.choice(possibleTerrains)
            terrainMap[i][j] = Terrain(choiceTerrainEnums.NAME, i, j, choiceTerrainEnums.DEFENSEBONUS, choiceTerrainEnums.MOVEMENTPENALTY)

terrainMap[1][4] = Building(1, 4, Player.PLAYER_1)
terrainMap[7][7] = Building(7, 7, Player.NEUTRAL)
terrainMap[14][14] = Building(14, 14, Player.PLAYER_2)


class defaultBoard:
    white_pieces = white_pieces
    black_pieces = black_pieces
    board = board
    terrain = terrainMap
