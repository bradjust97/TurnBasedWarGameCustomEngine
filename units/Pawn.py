# Pawn
from Piece import Piece
from enums import PawnEnums, Player


class Pawn(Piece):
    def __init__(self, row_number, col_number, player):
        name = PawnEnums.NAME
        super().__init__(name, row_number, col_number, player)

    def get_valid_piece_takes(self, game_state):
        _moves = []
        row_change = [-1, +0, +1, -1, +1, -1, +0, +1]
        col_change = [-1, -1, -1, +0, +0, +1, +1, +1]

        for i in range(0, len(row_change)):
            new_row = self.get_row_number() + row_change[i]
            new_col = self.get_col_number() + col_change[i]
            evaluating_square = game_state.get_piece(new_row, new_col)
            # when the square with new_row and new_col contains a valid piece
            if game_state.is_valid_piece(new_row, new_col):
                # when the king is white and the piece near the king is black
                if self.is_player(Player.PLAYER_1) and evaluating_square.is_player(Player.PLAYER_2):
                    _moves.append((new_row, new_col))
                # when the king is black and the piece near the king is white
                elif self.is_player(Player.PLAYER_2) and evaluating_square.is_player(Player.PLAYER_1):
                    _moves.append((new_row, new_col))
        return _moves

    def get_valid_peaceful_moves(self, game_state):
        _moves = []
        row_change = [-1, +0, +1, -1, +1, -1, +0, +1]
        col_change = [-1, -1, -1, +0, +0, +1, +1, +1] #BJUSTICE THIS FAILS AFTER MOVE IS DONE AND ITS TRYING TO CALC NEXT POSSIBLE MOVES. THIS IS BECAUSE THE 
                                                      # ORIGINAL RETARD WHO CODED THIS HARD CODED POSSIBLE MOVES FOR KING AND KNIGHT. SQUAREBOARD DIMENSIONS DID
                                                      # NOT REPLACE THE BOARD DIMENSIONS BUT THE AMOUNT OF MOVES THE KING CAN DO. LOL. SQ DIMS IS 16, BUT THE ROWCHANGE
                                                      # ARRAY IS OF LEN 8

        for i in range(0, len(row_change)):
            new_row = self.get_row_number() + row_change[i]
            new_col = self.get_col_number() + col_change[i]
            evaluating_square = game_state.get_piece(new_row, new_col)
            # when the square with new_row and new_col is empty
            if evaluating_square == Player.EMPTY:
                _moves.append((new_row, new_col))

        return _moves

    def get_valid_piece_moves(self, game_state):
        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)
