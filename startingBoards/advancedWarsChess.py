# Initialize White pieces
from Piece import Bishop, King, Knight, Pawn, Queen, Rook
from enums import Player, SquareBoard


white_rook_1 = Rook('tank', 0, 0, Player.PLAYER_1)
white_knight_1 = Knight('artillery', 0, 1, Player.PLAYER_1)
white_bishop_1 = Bishop('recon', 0, 2, Player.PLAYER_1)
white_queen = Queen('queen', 0, 4, Player.PLAYER_1)
white_king = King('king', 0, 3, Player.PLAYER_1)
white_pawn_1 = Pawn('infantry', 1, 0, Player.PLAYER_1)
white_pawn_2 = Pawn('infantry', 1, 1, Player.PLAYER_1)
white_pawn_3 = Pawn('infantry', 1, 2, Player.PLAYER_1)
white_pawn_4 = Pawn('infantry', 1, 3, Player.PLAYER_1)
white_pawn_5 = Pawn('infantry', 1, 4, Player.PLAYER_1)
white_pieces = [white_rook_1, white_knight_1, white_bishop_1,
                        white_queen, white_king, white_pawn_1, white_pawn_2, white_pawn_3, white_pawn_4, white_pawn_5]

# Initialize Black Pieces
black_rook_2 = Rook('tank', 15, 15, Player.PLAYER_2)
black_knight_2 = Knight('artillery', 15, 14, Player.PLAYER_2)
black_bishop_2 = Bishop('recon', 15, 13, Player.PLAYER_2)
black_queen = Queen('queen', 15, 12, Player.PLAYER_2)
black_king = King('king', 15, 11, Player.PLAYER_2)
black_pawn_4 = Pawn('infantry', 14, 11, Player.PLAYER_2)
black_pawn_5 = Pawn('infantry', 14, 12, Player.PLAYER_2)
black_pawn_6 = Pawn('infantry', 14, 13, Player.PLAYER_2)
black_pawn_7 = Pawn('infantry', 14, 14, Player.PLAYER_2)
black_pawn_8 = Pawn('infantry', 14, 15, Player.PLAYER_2)
black_pieces = [ black_rook_2, black_knight_2, black_bishop_2,
                        black_queen, black_king, black_pawn_4,
                        black_pawn_5,
                        black_pawn_6, black_pawn_7, black_pawn_8]

board = [[Player.EMPTY for x in range(SquareBoard.DIMENSIONS)] for y in range(SquareBoard.DIMENSIONS)] 

for piece in white_pieces:
    board[piece.get_row_number()][piece.get_col_number()] = piece
for piece in black_pieces:
    board[piece.get_row_number()][piece.get_col_number()] = piece

class advancedWarsChess:
    white_pieces = white_pieces
    black_pieces = black_pieces
    board = board