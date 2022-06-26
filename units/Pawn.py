# Pawn
import itertools
from Piece import Piece
from combat_engine import get_pieces_within_range
from enums import PawnEnums, Player
from movement_engine import blocked_movement_diamond, make_movement_diamond


class Pawn(Piece):
    def __init__(self, row_number, col_number, player):
        name = PawnEnums.NAME
        movement = PawnEnums.MOVEMENT
        super().__init__(name, row_number, col_number, player, movement)

    def get_valid_piece_takes(self, game_state):
        _moves = []
        possible_moves = make_movement_diamond(PawnEnums.MOVEMENT)

        for i in range(0, len(possible_moves)):
            new_row = self.get_row_number() + possible_moves[i][0]
            new_col = self.get_col_number() + possible_moves[i][1]
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
        possible_moves = make_movement_diamond(PawnEnums.MOVEMENT)

        # list(itertools.product(row_change, col_change))
        for i in range(0, len(possible_moves)):
            new_row = self.get_row_number() + possible_moves[i][0]
            new_col = self.get_col_number() + possible_moves[i][1]
            evaluating_square = game_state.get_piece(new_row, new_col)
            # when the square with new_row and new_col is empty
            if evaluating_square == Player.EMPTY:
                _moves.append((new_row, new_col))

        return _moves

    def get_valid_piece_moves(self, game_state):
        #total_moves = self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)
        # return total_moves
        return blocked_movement_diamond(PawnEnums.MOVEMENT, self.get_row_number(), self.get_col_number(), game_state)
    

        #pieces_within_range = get_pieces_within_range(self, game_state)
