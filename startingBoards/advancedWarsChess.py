from enums import Player, RoadEnums, SquareBoard, TerrainEnums
from terrain.Building import Building
from terrain.Terrain import Terrain
from units.King import King
from units.ScoutCavalry import ScoutCavalry
from units.Catapult import Catapult
from units.Knight import Knight
from units.Footman import Footman
import random

white_knight_1 = Knight(14, 0, Player.PLAYER_1)
white_knight_2 = Knight(15, 0, Player.PLAYER_1)
white_catapult_1 = Catapult(0, 1, Player.PLAYER_1)
white_scoutCavalry_1 = ScoutCavalry(0, 2, Player.PLAYER_1)
white_king = King(0, 3, Player.PLAYER_1)
white_footman_1 = Footman(1, 0, Player.PLAYER_1)
white_footman_2 = Footman(1, 1, Player.PLAYER_1)
white_footman_3 = Footman(1, 2, Player.PLAYER_1)
white_footman_4 = Footman(1, 3, Player.PLAYER_1)
white_footman_5 = Footman(1, 4, Player.PLAYER_1)
white_pieces = [white_footman_2, white_footman_1, white_knight_1, white_knight_2] #, white_catapult_1, white_scoutCavalry_1,
# white_pieces = [white_knight_1, white_catapult_1, white_scoutCavalry_1,
#                          white_king, white_footman_1, white_footman_2, white_footman_3, white_footman_4, white_footman_5] #white_queen,

# Initialize Black Pieces
black_knight_2 = Knight(0, 15, Player.PLAYER_2)
black_knight_3 = Knight(0, 14, Player.PLAYER_2)
black_catapult_2 = Catapult(15, 14, Player.PLAYER_2)
black_scoutCavalry_2 = ScoutCavalry(15, 13, Player.PLAYER_2)
black_king = King(15, 11, Player.PLAYER_2)
black_footman_4 = Footman(14, 11, Player.PLAYER_2)
black_footman_5 = Footman(14, 12, Player.PLAYER_2)
black_footman_6 = Footman(14, 13, Player.PLAYER_2)
black_footman_7 = Footman(14, 14, Player.PLAYER_2)
black_footman_8 = Footman(14, 15, Player.PLAYER_2)
black_pieces = [ black_footman_4, black_footman_5, black_knight_2, black_knight_3]
# black_pieces = [ black_knight_2, black_catapult_2, black_scoutCavalry_2,
#                          black_king, black_footman_4,
#                         black_footman_5,
#                         black_footman_6, black_footman_7, black_footman_8, black_knight_3]  #black_queen,

board = [[Player.EMPTY for x in range(SquareBoard.DIMENSIONS)] for y in range(SquareBoard.DIMENSIONS)] 


for piece in white_pieces:
    board[piece.get_row_number()][piece.get_col_number()] = piece
for piece in black_pieces:
    board[piece.get_row_number()][piece.get_col_number()] = piece

terrainMap = [[Terrain(TerrainEnums.ROAD.NAME, y, x, TerrainEnums.ROAD.DEFENSEBONUS, TerrainEnums.ROAD.MOVEMENTPENALTY) for x in range(SquareBoard.DIMENSIONS)] for y in range(SquareBoard.DIMENSIONS)] 

possibleTerrains = [TerrainEnums.PLAINS, TerrainEnums.FOREST, TerrainEnums.PLAINS, TerrainEnums.FOREST,TerrainEnums.MOUNTAIN]

for i in range(SquareBoard.DIMENSIONS):
    for j in range(SquareBoard.DIMENSIONS):
        if i > 2 and i < SquareBoard.DIMENSIONS - 3:
             choiceTerrainEnums = random.choice(possibleTerrains)
             terrainMap[i][j] = Terrain(choiceTerrainEnums.NAME, i, j, choiceTerrainEnums.DEFENSEBONUS, choiceTerrainEnums.MOVEMENTPENALTY)

terrainMap[1][4] = Building(1,4, Player.PLAYER_1)
terrainMap[7][7] = Building(7,7, Player.NEUTRAL)
terrainMap[14][14] = Building(14,14, Player.PLAYER_2)

class advancedWarsChess:
    white_pieces = white_pieces
    black_pieces = black_pieces
    board = board
    terrain = terrainMap