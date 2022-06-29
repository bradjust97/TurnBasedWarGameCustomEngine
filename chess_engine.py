#
# The Chess Board class
# Will store the state of the chess game, print the chess board, find valid moves, store move logs.
#
# Note: move log class inspired by Eddie Sharick
#
from operator import xor
from Piece import Piece
from combat_engine import get_pieces_within_range
from enums import Player, PostmoveOptions, SquareBoard
from startingBoards.advancedWarsChess import advancedWarsChess

'''
r \ c     0           1           2           3           4           5           6           7 
0   [(r=0, c=0), (r=0, c=1), (r=0, c=2), (r=0, c=3), (r=0, c=4), (r=0, c=5), (r=0, c=6), (r=0, c=7)]
1   [(r=1, c=0), (r=1, c=1), (r=1, c=2), (r=1, c=3), (r=1, c=4), (r=1, c=5), (r=1, c=6), (r=1, c=7)]
2   [(r=2, c=0), (r=2, c=1), (r=2, c=2), (r=2, c=3), (r=2, c=4), (r=2, c=5), (r=2, c=6), (r=2, c=7)]
3   [(r=3, c=0), (r=3, c=1), (r=3, c=2), (r=3, c=3), (r=3, c=4), (r=3, c=5), (r=3, c=6), (r=3, c=7)]
4   [(r=4, c=0), (r=4, c=1), (r=4, c=2), (r=4, c=3), (r=4, c=4), (r=4, c=5), (r=4, c=6), (r=4, c=7)]
5   [(r=5, c=0), (r=5, c=1), (r=5, c=2), (r=5, c=3), (r=5, c=4), (r=5, c=5), (r=5, c=6), (r=5, c=7)]
6   [(r=6, c=0), (r=6, c=1), (r=6, c=2), (r=6, c=3), (r=6, c=4), (r=6, c=5), (r=6, c=6), (r=6, c=7)]
7   [(r=7, c=0), (r=7, c=1), (r=7, c=2), (r=7, c=3), (r=7, c=4), (r=7, c=5), (r=7, c=6), (r=7, c=7)]
'''


class game_state:
    # Initialize 2D array to represent the chess board
    def __init__(self):
        # The board is a 2D array
        # TODO: Change to a numpy format later
        self.white_captives = []
        self.black_captives = []
        self.move_log = []
        self.white_turn = True
        self.checkmate = False
        self.stalemate = False
        self.white_is_dead = False
        self.black_is_dead = False

        self._white_king_location = [0, 3]
        self._black_king_location = [7, 3]

        self.white_pieces = advancedWarsChess.white_pieces
        self.black_pieces = advancedWarsChess.black_pieces
        self.board = advancedWarsChess.board
        self.moved_pieces = [] 

    def end_turn(self):
        print("Ending turn")
        self.white_turn = not self.white_turn

    def get_piece(self, row, col):
        if (0 <= row < SquareBoard.DIMENSIONS) and (0 <= col < SquareBoard.DIMENSIONS):
            return self.board[row][col]
    
    def remove_piece(self, piece):
        self.board[piece.get_row_number()][piece.get_col_number()] = Player.EMPTY

    # returns if player piece
    def is_valid_piece(self, row, col):
        evaluated_piece = self.get_piece(row, col)
        return (evaluated_piece is not None) and (evaluated_piece != Player.EMPTY) and (evaluated_piece != Player.WALL)
    
    def is_wall(self, row, col):
        evaluated_piece = self.get_piece(row, col)
        return (evaluated_piece == Player.WALL)
    
    def is_empty(self, row, col):
        evaluated_piece = self.get_piece(row, col)
        return (evaluated_piece == Player.EMPTY)

    def get_valid_moves(self, starting_square):
        # i dont trust this method
        current_row = starting_square[0]
        current_col = starting_square[1]

        if self.is_valid_piece(current_row, current_col):
            moving_piece = self.get_piece(current_row, current_col)
            initial_valid_piece_moves = moving_piece.get_valid_piece_moves(self)
            return initial_valid_piece_moves
        else:
            return None
    
    def piece_moved(self, piece: Piece):
        self.moved_pieces.append(piece)

    def has_piece_moved(self, piece):
        return piece in self.moved_pieces
    
    def reset_moved_pieces(self):
        print("Reseting moved pieces")
        self.moved_pieces = []

    # 0 if white lost, 1 if black lost, 2 if stalemate, 3 if not game over
    def checkmate_stalemate_checker(self):
        all_white_moves = self.get_all_legal_moves(Player.PLAYER_1)
        all_black_moves = self.get_all_legal_moves(Player.PLAYER_2)
        if self.whose_turn() and not all_white_moves:
            print("white lost")
            return 0
        elif not self.whose_turn() and not all_black_moves:
            print("black lost")
            return 1
        elif not all_white_moves and not all_black_moves:
            return 2
        else:
            return 3
    
    def isDeadKing(self):
        if self.white_is_dead:
            print("Black Wins!")
            return 0
        elif self.black_is_dead:
            print ("White Wins!")
            return 1

    def get_all_legal_moves(self, player):
        _all_valid_moves = []
        for row in range(0, SquareBoard.DIMENSIONS):
            for col in range(0, SquareBoard.DIMENSIONS):
                if self.is_valid_piece(row, col) and self.get_piece(row, col).is_player(player):
                    valid_moves = self.get_valid_moves((row, col))
                    for move in valid_moves:
                        _all_valid_moves.append(((row, col), move))
        return _all_valid_moves

    # Move a piece
    def move_piece(self, starting_square, ending_square):
        current_square_row = starting_square[0]  # The integer row value of the starting square
        current_square_col = starting_square[1]  # The integer col value of the starting square
        next_square_row = ending_square[0]  # The integer row value of the ending square
        next_square_col = ending_square[1]  # The integer col value of the ending square

        if self.is_valid_piece(current_square_row, current_square_col) and \
            not self.has_piece_moved(self.get_piece(current_square_row, current_square_col)) and \
                ((self.whose_turn() and self.get_piece(current_square_row, current_square_col).is_player(Player.PLAYER_1)) or
                  (not self.whose_turn() and self.get_piece(current_square_row, current_square_col).is_player(Player.PLAYER_2))):

            if (starting_square == ending_square):
                self.piece_moved(self.get_piece(current_square_row, current_square_col))
                return

            # The chess piece at the starting square
            moving_piece = self.get_piece(current_square_row, current_square_col)

            # TODO may be unecessary if calcd via UI
            valid_moves = self.get_valid_moves(starting_square)

            temp = True

            if ending_square in valid_moves:
                moved_to_piece = self.get_piece(next_square_row, next_square_col)
                if moved_to_piece != -9:
                    if moved_to_piece.get_name() == "king" and self.whose_turn():
                        self.black_is_dead = True
                    elif moved_to_piece.get_name() == "king" and not self.whose_turn():
                        self.white_is_dead = True
                self.move_log.append(chess_move(starting_square, ending_square, self))

                if temp:
                    moving_piece.change_row_number(next_square_row)
                    moving_piece.change_col_number(next_square_col)
                    self.board[next_square_row][next_square_col] = self.board[current_square_row][current_square_col]
                    self.board[current_square_row][current_square_col] = Player.EMPTY

                self.piece_moved(moving_piece)
                #self.white_turn = not self.white_turn

            else:
                pass
    
    def attack_piece(self, attacker: Piece, defender: Piece):
        defenderDied = attacker.standard_attack(defender)
        if defenderDied:
            self.remove_piece(defender)
    
    def get_postmove_options(self, piece):
        options = [PostmoveOptions.WAIT]
        attackableEnemies = get_pieces_within_range(piece, self) 
        # TODO eventually abstract all detection methods on determining if an option is available or not
        if (len(attackableEnemies) != 0):
            options.append(PostmoveOptions.ATTACK)
        print("Returning postmove options")
        return options

    # true if white, false if black
    def whose_turn(self):
        return self.white_turn

    def is_current_players_piece(self, piece):
        # this is NAND
        print("whose turn:")
        print(self.whose_turn())
        print("whose piece:")
        print(piece.get_player() == Player.PLAYER_1)
        return self.whose_turn() == (piece.get_player() == Player.PLAYER_1)


class chess_move():
    def __init__(self, starting_square, ending_square, game_state):
        self.starting_square_row = starting_square[0]
        self.starting_square_col = starting_square[1]
        self.moving_piece = game_state.get_piece(self.starting_square_row, self.starting_square_col)

        self.ending_square_row = ending_square[0]
        self.ending_square_col = ending_square[1]
        if game_state.is_valid_piece(self.ending_square_row, self.ending_square_col):
            self.removed_piece = game_state.get_piece(self.ending_square_row, self.ending_square_col)
        else:
            self.removed_piece = Player.EMPTY

        self.rook_starting_square = None
        self.rook_ending_square = None
        self.moving_rook = None

        self.pawn_promoted = False
        self.replacement_piece = None

    def get_moving_piece(self):
        return self.moving_piece
