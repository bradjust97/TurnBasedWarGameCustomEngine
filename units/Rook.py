# Rook (R)
from Piece import Piece
from enums import Player, RookEnums, SquareBoard


class Rook(Piece):
    def __init__(self, row_number, col_number, player):
        name = RookEnums.NAME
        super().__init__(name, row_number, col_number, player)
        self.has_moved = False

    def get_valid_peaceful_moves(self, game_state):
        return self.traverse(game_state)[0]

    def get_valid_piece_takes(self, game_state):
        return self.traverse(game_state)[1]

    def get_valid_piece_moves(self, game_state):
        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)

    def traverse(self, game_state):
        _peaceful_moves = []
        _piece_takes = []

        self._up = 1
        self._down = 1
        self._left = 1
        self._right = 1

        # Left of the Rook
        self._breaking_point = False
        while self.get_col_number() - self._left >= 0 and not self._breaking_point:
            # when the square to the left is empty
            if game_state.get_piece(self.get_row_number(), self.get_col_number() - self._left) is Player.EMPTY:
                _peaceful_moves.append((self.get_row_number(), self.get_col_number() - self._left))
                self._left += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(self.get_row_number(), self.get_col_number() - self._left) and \
                    not game_state.get_piece(self.get_row_number(), self.get_col_number() - self._left).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number(), self.get_col_number() - self._left))
                self._breaking_point = True
            else:
                self._breaking_point = True

        # Right of the Rook
        self._breaking_point = False
        while self.get_col_number() + self._right < SquareBoard.DIMENSIONS and not self._breaking_point:
            # when the square to the left is empty
            if game_state.get_piece(self.get_row_number(), self.get_col_number() + self._right) is Player.EMPTY:
                _peaceful_moves.append((self.get_row_number(), self.get_col_number() + self._right))
                self._right += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(self.get_row_number(), self.get_col_number() + self._right) and \
                    not game_state.get_piece(self.get_row_number(), self.get_col_number() + self._right).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number(), self.get_col_number() + self._right))
                self._breaking_point = True
            else:
                self._breaking_point = True

        # Below the Rook
        self._breaking_point = False
        while self.get_row_number() + self._down < SquareBoard.DIMENSIONS and not self._breaking_point:
            # when the square to the left is empty
            if game_state.get_piece(self.get_row_number() + self._down, self.get_col_number()) is Player.EMPTY:
                _peaceful_moves.append((self.get_row_number() + self._down, self.get_col_number()))
                self._down += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(self.get_row_number() + self._down, self.get_col_number()) and \
                    not game_state.get_piece(self.get_row_number() + self._down, self.get_col_number()).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number() + self._down, self.get_col_number()))
                self._breaking_point = True
            else:
                self._breaking_point = True

        # Above the Rook
        self._breaking_point = False
        while self.get_row_number() - self._up >= 0 and not self._breaking_point:
            # when the square to the left is empty
            if game_state.get_piece(self.get_row_number() - self._up, self.get_col_number()) is Player.EMPTY:
                _peaceful_moves.append((self.get_row_number() - self._up, self.get_col_number()))
                self._up += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(self.get_row_number() - self._up, self.get_col_number()) and \
                    not game_state.get_piece(self.get_row_number() - self._up, self.get_col_number()).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number() - self._up, self.get_col_number()))
                self._breaking_point = True
            else:
                self._breaking_point = True
        return (_peaceful_moves, _piece_takes)
