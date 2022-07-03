from Piece import Piece
from enums import ScoutCavalryEnums, Player, SquareBoard
from movement_engine import blocked_movement_diamond, make_movement_diamond


class ScoutCavalry(Piece):
    def __init__(self, row_number, col_number, player):
        name = ScoutCavalryEnums.NAME
        movement = ScoutCavalryEnums.MOVEMENT
        super().__init__(name, row_number, col_number, player, movement)

    def get_valid_piece_takes(self, game_state):
        _moves = []
        possible_moves = make_movement_diamond(ScoutCavalryEnums.MOVEMENT)

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
        possible_moves = make_movement_diamond(ScoutCavalryEnums.MOVEMENT)

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
        return blocked_movement_diamond(ScoutCavalryEnums.MOVEMENT, self.get_row_number(), self.get_col_number(), game_state)
        #return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)

    # def traverse(self, game_state):
    #     _peaceful_moves = []
    #     _piece_takes = []

    #     self._breaking_point = False
    #     self._up = 1
    #     self._down = 1
    #     self._left = 1
    #     self._right = 1
    #     while self.get_col_number() - self._left >= 0 and self.get_row_number() - self._up >= 0 and not self._breaking_point:
    #         # when the square is empty
    #         if game_state.get_piece(self.get_row_number() - self._up, self.get_col_number() - self._left) is Player.EMPTY:
    #             _peaceful_moves.append((self.get_row_number() - self._up, self.get_col_number() - self._left))
    #             self._left += 1
    #             self._up += 1
    #         # when the square contains an opposing piece
    #         elif game_state.is_valid_piece(self.get_row_number() - self._up, self.get_col_number() - self._left) and \
    #                 not game_state.get_piece(self.get_row_number() - self._up, self.get_col_number() - self._left).is_player(self.get_player()):
    #             _piece_takes.append((self.get_row_number() - self._up, self.get_col_number() - self._left))
    #             self._breaking_point = True
    #         else:
    #             self._breaking_point = True

    #     # Right up of the ScoutCavalry
    #     self._breaking_point = False
    #     self._up = 1
    #     self._down = 1
    #     self._left = 1
    #     self._right = 1
    #     while self.get_col_number() + self._right < SquareBoard.DIMENSIONS and self.get_row_number() - self._up >= 0 and not self._breaking_point:
    #         # when the square is empty
    #         if game_state.get_piece(self.get_row_number() - self._up, self.get_col_number() + self._right) is Player.EMPTY:
    #             _peaceful_moves.append((self.get_row_number() - self._up, self.get_col_number() + self._right))
    #             self._right += 1
    #             self._up += 1
    #         # when the square contains an opposing piece
    #         elif game_state.is_valid_piece(self.get_row_number() - self._up, self.get_col_number() + self._right) and \
    #                 not game_state.get_piece(self.get_row_number() - self._up, self.get_col_number() + self._right).is_player(self.get_player()):
    #             _piece_takes.append((self.get_row_number() - self._up, self.get_col_number() + self._right))
    #             self._breaking_point = True
    #         else:
    #             self._breaking_point = True

    #     # Down left of the ScoutCavalry
    #     self._breaking_point = False
    #     self._up = 1
    #     self._down = 1
    #     self._left = 1
    #     self._right = 1
    #     while self.get_col_number() - self._left >= 0 and self.get_row_number() + self._down < SquareBoard.DIMENSIONS and not self._breaking_point:
    #         # when the square is empty
    #         if game_state.get_piece(self.get_row_number() + self._down, self.get_col_number() - self._left) is Player.EMPTY:
    #             _peaceful_moves.append((self.get_row_number() + self._down, self.get_col_number() - self._left))
    #             self._down += 1
    #             self._left += 1
    #         # when the square contains an opposing piece
    #         elif game_state.is_valid_piece(self.get_row_number() + self._down, self.get_col_number() - self._left) and \
    #                 not game_state.get_piece(self.get_row_number() + self._down, self.get_col_number() - self._left).is_player(self.get_player()):
    #             _piece_takes.append((self.get_row_number() + self._down, self.get_col_number() - self._left))
    #             self._breaking_point = True
    #         else:
    #             self._breaking_point = True

    #     # Down right of the ScoutCavalry
    #     self._breaking_point = False
    #     self._up = 1
    #     self._down = 1
    #     self._left = 1
    #     self._right = 1
    #     while self.get_col_number() + self._right < SquareBoard.DIMENSIONS and self.get_row_number() + self._down < SquareBoard.DIMENSIONS and not self._breaking_point:
    #         # when the square is empty
    #         if game_state.get_piece(self.get_row_number() + self._down, self.get_col_number() + self._right) is Player.EMPTY:
    #             _peaceful_moves.append((self.get_row_number() + self._down, self.get_col_number() + self._right))
    #             self._down += 1
    #             self._right += 1
    #         # when the square contains an opposing piece
    #         elif game_state.is_valid_piece(self.get_row_number() + self._down, self.get_col_number() + self._right) and \
    #                 not game_state.get_piece(self.get_row_number() + self._down, self.get_col_number() + self._right).is_player(
    #                     self.get_player()):
    #             _piece_takes.append((self.get_row_number() + self._down, self.get_col_number() + self._right))
    #             self._breaking_point = True
    #         else:
    #             self._breaking_point = True
        return (_peaceful_moves, _piece_takes)
