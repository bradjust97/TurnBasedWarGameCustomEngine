# Bishop
from Piece import Piece
from enums import Player, SquareBoard


class Bishop(Piece):
    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)

    def get_valid_piece_takes(self, game_state):
        return self.traverse(game_state)[1]

    def get_valid_peaceful_moves(self, game_state):
        return self.traverse(game_state)[0]

    def get_valid_piece_moves(self, game_state):
        return self.get_valid_piece_takes(game_state) + self.get_valid_peaceful_moves(game_state)

    def traverse(self, game_state):
        _peaceful_moves = []
        _piece_takes = []

        self._breaking_point = False
        self._up = 1
        self._down = 1
        self._left = 1
        self._right = 1
        while self.get_col_number() - self._left >= 0 and self.get_row_number() - self._up >= 0 and not self._breaking_point:
            # when the square is empty
            if game_state.get_piece(self.get_row_number() - self._up, self.get_col_number() - self._left) is Player.EMPTY:
                _peaceful_moves.append((self.get_row_number() - self._up, self.get_col_number() - self._left))
                self._left += 1
                self._up += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(self.get_row_number() - self._up, self.get_col_number() - self._left) and \
                    not game_state.get_piece(self.get_row_number() - self._up, self.get_col_number() - self._left).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number() - self._up, self.get_col_number() - self._left))
                self._breaking_point = True
            else:
                self._breaking_point = True

        # Right up of the bishop
        self._breaking_point = False
        self._up = 1
        self._down = 1
        self._left = 1
        self._right = 1
        while self.get_col_number() + self._right < SquareBoard.DIMENSIONS and self.get_row_number() - self._up >= 0 and not self._breaking_point:
            # when the square is empty
            if game_state.get_piece(self.get_row_number() - self._up, self.get_col_number() + self._right) is Player.EMPTY:
                _peaceful_moves.append((self.get_row_number() - self._up, self.get_col_number() + self._right))
                self._right += 1
                self._up += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(self.get_row_number() - self._up, self.get_col_number() + self._right) and \
                    not game_state.get_piece(self.get_row_number() - self._up, self.get_col_number() + self._right).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number() - self._up, self.get_col_number() + self._right))
                self._breaking_point = True
            else:
                self._breaking_point = True

        # Down left of the bishop
        self._breaking_point = False
        self._up = 1
        self._down = 1
        self._left = 1
        self._right = 1
        while self.get_col_number() - self._left >= 0 and self.get_row_number() + self._down < SquareBoard.DIMENSIONS and not self._breaking_point:
            # when the square is empty
            if game_state.get_piece(self.get_row_number() + self._down, self.get_col_number() - self._left) is Player.EMPTY:
                _peaceful_moves.append((self.get_row_number() + self._down, self.get_col_number() - self._left))
                self._down += 1
                self._left += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(self.get_row_number() + self._down, self.get_col_number() - self._left) and \
                    not game_state.get_piece(self.get_row_number() + self._down, self.get_col_number() - self._left).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number() + self._down, self.get_col_number() - self._left))
                self._breaking_point = True
            else:
                self._breaking_point = True

        # Down right of the bishop
        self._breaking_point = False
        self._up = 1
        self._down = 1
        self._left = 1
        self._right = 1
        while self.get_col_number() + self._right < SquareBoard.DIMENSIONS and self.get_row_number() + self._down < SquareBoard.DIMENSIONS and not self._breaking_point:
            # when the square is empty
            if game_state.get_piece(self.get_row_number() + self._down, self.get_col_number() + self._right) is Player.EMPTY:
                _peaceful_moves.append((self.get_row_number() + self._down, self.get_col_number() + self._right))
                self._down += 1
                self._right += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(self.get_row_number() + self._down, self.get_col_number() + self._right) and \
                    not game_state.get_piece(self.get_row_number() + self._down, self.get_col_number() + self._right).is_player(
                        self.get_player()):
                _piece_takes.append((self.get_row_number() + self._down, self.get_col_number() + self._right))
                self._breaking_point = True
            else:
                self._breaking_point = True
        return (_peaceful_moves, _piece_takes)
