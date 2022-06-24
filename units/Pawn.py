# Pawn
from Piece import Piece
from enums import PawnEnums, Player


class Pawn(Piece):
    def __init__(self, row_number, col_number, player):
        name = PawnEnums.NAME
        super().__init__(name, row_number, col_number, player)

    def get_valid_piece_takes(self, game_state):
        _moves = []
        if self.is_player(Player.PLAYER_1):
            # when the square to the bottom left of the starting_square has a black piece
            if game_state.is_valid_piece(self.get_row_number() + 1, self.get_col_number() - 1) and \
                    game_state.get_piece(self.get_row_number() + 1, self.get_col_number() - 1).is_player(Player.PLAYER_2):
                _moves.append((self.get_row_number() + 1, self.get_col_number() - 1))
            # when the square to the bottom right of the starting_square has a black piece
            if game_state.is_valid_piece(self.get_row_number() + 1, self.get_col_number() + 1) and \
                    game_state.get_piece(self.get_row_number() + 1, self.get_col_number() + 1).is_player(Player.PLAYER_2):
                _moves.append((self.get_row_number() + 1, self.get_col_number() + 1))
            if game_state.can_en_passant(self.get_row_number(), self.get_col_number()):
                _moves.append((self.get_row_number() + 1, game_state.previous_piece_en_passant()[1]))
        # when the pawn is a black piece
        elif self.is_player(Player.PLAYER_2):
            # when the square to the top left of the starting_square has a white piece
            if game_state.is_valid_piece(self.get_row_number() - 1, self.get_col_number() - 1) and \
                    game_state.get_piece(self.get_row_number() - 1, self.get_col_number() - 1).is_player(Player.PLAYER_1):
                _moves.append((self.get_row_number() - 1, self.get_col_number() - 1))
            # when the square to the top right of the starting_square has a white piece
            if game_state.is_valid_piece(self.get_row_number() - 1, self.get_col_number() + 1) and \
                    game_state.get_piece(self.get_row_number() - 1, self.get_col_number() + 1).is_player(Player.PLAYER_1):
                _moves.append((self.get_row_number() - 1, self.get_col_number() + 1))
            if game_state.can_en_passant(self.get_row_number(), self.get_col_number()):
                _moves.append((self.get_row_number() - 1, game_state.previous_piece_en_passant()[1]))
        return _moves

    def get_valid_peaceful_moves(self, game_state):
        _moves = []
        # when the pawn is a white piece
        if self.is_player(Player.PLAYER_1):
            # when the square right below the starting_square is empty
            if game_state.get_piece(self.get_row_number() + 1, self.get_col_number()) == Player.EMPTY:
                _moves.append((self.get_row_number() + 1, self.get_col_number()))
        # when the pawn is a black piece
        elif self.is_player(Player.PLAYER_2):
            # when the square right above is empty
            if game_state.get_piece(self.get_row_number() - 1, self.get_col_number()) == Player.EMPTY:
                _moves.append((self.get_row_number() - 1, self.get_col_number()))
        return _moves

    def get_valid_piece_moves(self, game_state):
        # current_square_row = self.row_number  # The integer row value of the starting square
        # current_square_col = self.col_number  # The integer col value of the starting square
        #
        # _moves = []# self._moves.clear()
        # # when the pawn is a white piece
        # if self.is_player(Player.PLAYER_1):
        #     # when the square right below the starting_square is empty
        #     if game_state.get_piece(current_square_row + 1, current_square_col) == Player.EMPTY:
        #         # when the pawn has not been moved yet
        #         if self.get_row_number() == 1 and game_state.get_piece(current_square_row +2, current_square_col) == Player.EMPTY:
        #             _moves.append((current_square_row + 1, current_square_col))
        #             _moves.append((current_square_row + 2, current_square_col))
        #         # when the pawn has already been moved
        #         else:
        #             _moves.append((current_square_row + 1, current_square_col))
        #     # when the square to the bottom left of the starting_square has a black piece
        #     if game_state.is_valid_piece(current_square_row + 1, current_square_col - 1) and \
        #             game_state.get_piece(current_square_row + 1, current_square_col - 1).is_player(Player.PLAYER_2):
        #         _moves.append((current_square_row + 1, current_square_col - 1))
        #     # when the square to the bottom right of the starting_square has a black piece
        #     if game_state.is_valid_piece(current_square_row + 1, current_square_col + 1) and \
        #             game_state.get_piece(current_square_row + 1, current_square_col + 1).is_player(Player.PLAYER_2):
        #         _moves.append((current_square_row + 1, current_square_col + 1))
        #     if game_state.can_en_passant(current_square_row, current_square_col):
        #         _moves.append((current_square_row + 1, game_state.previous_piece_en_passant()[1]))
        # # when the pawn is a black piece
        # elif self.is_player(Player.PLAYER_2):
        #     # when the square right above is empty
        #     if game_state.get_piece(current_square_row - 1, current_square_col) == Player.EMPTY:
        #         # when the pawn has not been moved yet
        #         if self.get_row_number() == 6 and game_state.get_piece(current_square_row -2, current_square_col) == Player.EMPTY:
        #             _moves.append((current_square_row - 1, current_square_col))
        #             _moves.append((current_square_row - 2, current_square_col))
        #         # when the pawn has been moved
        #         else:
        #             _moves.append((current_square_row - 1, current_square_col))
        #     # when the square to the top left of the starting_square has a white piece
        #     if game_state.is_valid_piece(current_square_row - 1, current_square_col - 1) and \
        #             game_state.get_piece(current_square_row - 1, current_square_col - 1).is_player(Player.PLAYER_1):
        #         _moves.append((current_square_row - 1, current_square_col - 1))
        #     # when the square to the top right of the starting_square has a white piece
        #     if game_state.is_valid_piece(current_square_row - 1, current_square_col + 1) and \
        #             game_state.get_piece(current_square_row - 1, current_square_col + 1).is_player(Player.PLAYER_1):
        #         _moves.append((current_square_row - 1, current_square_col + 1))
        #     if game_state.can_en_passant(current_square_row, current_square_col):
        #         _moves.append((current_square_row - 1, game_state.previous_piece_en_passant()[1]))
        # return _moves
        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)
