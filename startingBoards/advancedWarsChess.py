from enums import Player, SquareBoard
from units.King import King
#from units.Queen import Queen
from units.Bishop import Bishop
from units.Knight import Knight
from units.Rook import Rook
from units.Pawn import Pawn
#from units import Bishop.Bishop, King, Queen, Knight, Rook, Pawn


white_rook_1 = Rook(0, 0, Player.PLAYER_1)
white_knight_1 = Knight(0, 1, Player.PLAYER_1)
white_bishop_1 = Bishop(0, 2, Player.PLAYER_1)
white_king = King(0, 3, Player.PLAYER_1)
white_pawn_1 = Pawn(1, 0, Player.PLAYER_1)
white_pawn_2 = Pawn(1, 1, Player.PLAYER_1)
white_pawn_3 = Pawn(1, 2, Player.PLAYER_1)
white_pawn_4 = Pawn(1, 3, Player.PLAYER_1)
white_pawn_5 = Pawn(1, 4, Player.PLAYER_1)
white_pieces = [white_rook_1, white_knight_1, white_bishop_1,
                         white_king, white_pawn_1, white_pawn_2, white_pawn_3, white_pawn_4, white_pawn_5] #white_queen,

# Initialize Black Pieces
black_rook_2 = Rook(15, 15, Player.PLAYER_2)
black_knight_2 = Knight(15, 14, Player.PLAYER_2)
black_bishop_2 = Bishop(15, 13, Player.PLAYER_2)
black_king = King(15, 11, Player.PLAYER_2)
black_pawn_4 = Pawn(14, 11, Player.PLAYER_2)
black_pawn_5 = Pawn(14, 12, Player.PLAYER_2)
black_pawn_6 = Pawn(14, 13, Player.PLAYER_2)
black_pawn_7 = Pawn(14, 14, Player.PLAYER_2)
black_pawn_8 = Pawn(14, 15, Player.PLAYER_2)
black_pieces = [ black_rook_2, black_knight_2, black_bishop_2,
                         black_king, black_pawn_4,
                        black_pawn_5,
                        black_pawn_6, black_pawn_7, black_pawn_8]  #black_queen,

board = [[Player.EMPTY for x in range(SquareBoard.DIMENSIONS)] for y in range(SquareBoard.DIMENSIONS)] 

for piece in white_pieces:
    board[piece.get_row_number()][piece.get_col_number()] = piece
for piece in black_pieces:
    board[piece.get_row_number()][piece.get_col_number()] = piece

class advancedWarsChess:
    white_pieces = white_pieces
    black_pieces = black_pieces
    board = board