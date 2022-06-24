#
# The Chess piece classes
#
# TODO: add checking if check after moving suggested move later

# General chess piece
from enums import Player, SquareBoard


class Piece:
    # Initialize the piece
    def __init__(self, name, row_number, col_number, player):
        self._name = name
        self.row_number = row_number
        self.col_number = col_number
        self._player = player

    # Get the x value
    def get_row_number(self):
        return self.row_number

    # Get the y value
    def get_col_number(self):
        return self.col_number

    # Get the name
    def get_name(self):
        return self._name

    def get_player(self):
        return self._player

    def is_player(self, player_checked):
        return self.get_player() == player_checked

    def can_move(self, board, starting_square):
        pass

    def can_take(self, is_check):
        pass

    def change_row_number(self, new_row_number):
        self.row_number = new_row_number

    def change_col_number(self, new_col_number):
        self.col_number = new_col_number

    def get_valid_piece_takes(self, game_state):
        pass

    def get_valid_peaceful_moves(self, game_state):
        pass

    # Get moves
    def get_valid_piece_moves(self, board):
        pass










