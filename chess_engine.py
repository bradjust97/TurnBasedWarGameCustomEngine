#
# The Game Board class
# Will store the state of the game, print the board, find valid moves, store move logs.
#
# Note: move log class inspired by Eddie Sharick
#
from typing import Type
from Piece import Piece
from combat_engine import get_pieces_within_range
from enums import DIMENSION, BuildingEnums, FundsEnums, Player, PostmoveOptionsEnums, SquareBoard, TerrainEnums
from startingBoards.advancedWarsChess import advancedWarsChess
from terrain.Building import Building

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
    # Initialize 2D array to represent the board
    def __init__(self):
        # The board is a 2D array
        # TODO: Change to a numpy format later
        self.move_log = []
        self.white_turn = True
        self.white_is_dead = False
        self.black_is_dead = False

        self._white_king_location = [0, 3]
        self._black_king_location = [7, 3]

        self.board = advancedWarsChess.board
        self.terrain = advancedWarsChess.terrain
        self.moved_pieces = [] 
        self.numBlackPieces = len(advancedWarsChess.black_pieces)
        self.numWhitePieces = len(advancedWarsChess.white_pieces)
        self.playerFunds = {Player.PLAYER_1 : 0, Player.PLAYER_2 : 0}

        self.runStartOfTurn()

    def end_turn(self):
        print("Ending turn")
        self.white_turn = not self.white_turn

    def get_piece(self, row, col):
        if (0 <= row < SquareBoard.DIMENSIONS) and (0 <= col < SquareBoard.DIMENSIONS):
            return self.board[row][col]
    
    # Technically dont need self
    def areAdjacent(self, piece1, piece2):
        r1 = piece1.get_row_number()
        c1 = piece1.get_col_number()
        r2 = piece2.get_row_number()
        c2 = piece2.get_col_number()

        # if they are the same row, then columns need to be adjacent
        if r1 == r2:
            if abs(c1 - c2) == 1:
                return True
        elif c1 == c2:
            if abs(r1 - r2) == 1:
                return True
        else:
            return False
    
    def get_terrain(self, row, col):
        # return a terrain given a [x,y]
        if (0 <= row < SquareBoard.DIMENSIONS) and (0 <= col < SquareBoard.DIMENSIONS):
            return self.terrain[row][col]
    
    def getTerrainNeighbors(self, row, col):
        # return a list of adjacent terrains given a x,y
        neighbors = [] 
        neighbors.append(self.get_terrain(row + 1, col))
        neighbors.append(self.get_terrain(row - 1, col))
        neighbors.append(self.get_terrain(row, col + 1))
        neighbors.append(self.get_terrain(row, col - 1))
        neighbors = [x for x in neighbors if x is not None]
        return neighbors
    
    def getNBlackPieces(self):
        return self.numBlackPieces
    
    def getNWhitePieces(self):
        return self.numWhitePieces
    
    def incrNBlackPieces(self, n=1):
        self.numBlackPieces = self.numBlackPieces + n

    def incrNWhitePieces(self, n=1):
        self.numWhitePieces = self.numWhitePieces + n

    def decrNBlackPieces(self, n=1):
        self.numBlackPieces = self.numBlackPieces - n

    def decrNWhitePieces(self, n=1):
        self.numWhitePieces = self.numWhitePieces - n
    
    def incrPieces(self, player, n=1):
        if (player == Player.PLAYER_1):
            self.incrNWhitePieces(n)
        else:
            self.incrNBlackPieces(n)
    
    def decrPieces(self, player, n=1):
        if (player == Player.PLAYER_1):
            self.decrNWhitePieces(n)
        else:
            self.decrNBlackPieces(n)
    
    def remove_piece(self, piece : Piece):
        player = piece.get_player()
        self.decrPieces(player)

        terrain = self.get_terrain(piece.get_row_number(), piece.get_col_number())
        unitWasOnBuilding = terrain.getTerrainName() == TerrainEnums.BUILDING.NAME
        if (unitWasOnBuilding):
            terrain.resetCapturePoints()

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
    
    def isDeadKing(self):
        if self.white_is_dead:
            print("Black Wins!")
            return 0
        elif self.black_is_dead:
            print ("White Wins!")
            return 1
    
    def noMorePiecesOfPlayer(self):
        if self.getNWhitePieces() == 0:
            return Player.PLAYER_1
        elif self.getNBlackPieces() == 0:
            return Player.PLAYER_2
        else:
            return Player.EMPTY
    
    def isGameEnd(self):
        if self.noMorePiecesOfPlayer() == Player.EMPTY:
            return (False, Player.EMPTY)
        else:
            return (True, self.noMorePiecesOfPlayer())

    def get_all_legal_moves(self, player):
        _all_valid_moves = []
        for row in range(0, SquareBoard.DIMENSIONS):
            for col in range(0, SquareBoard.DIMENSIONS):
                if self.is_valid_piece(row, col) and self.get_piece(row, col).is_player(player):
                    valid_moves = self.get_valid_moves((row, col))
                    for move in valid_moves:
                        _all_valid_moves.append(((row, col), move))
        return _all_valid_moves

    # Move a piece. Returns true is moved to the same spot it started
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
                return True

            # The unit at the starting square
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
                # self.move_log.append(chess_move(starting_square, ending_square, self))

                if temp:
                    moving_piece.change_row_number(next_square_row)
                    moving_piece.change_col_number(next_square_col)
                    self.board[next_square_row][next_square_col] = self.board[current_square_row][current_square_col]
                    self.board[current_square_row][current_square_col] = Player.EMPTY

                self.piece_moved(moving_piece)
                return False
            else:
                return False
    
    def attack_piece(self, attacker: Piece, defender: Piece):
        defenderTerrainDefenseValue = self.get_terrain(defender.get_row_number(), defender.get_col_number()).getDefenseBonus()
        defenderDied = attacker.standard_attack(defender, defenderTerrainDefenseValue)
        attackerDied = False
        if defenderDied:
            print("Defended died")
            self.remove_piece(defender)
        # Check for counterattack
        elif self.areAdjacent(attacker, defender) and defender.get_minRange() == 1:
            attackerTerrainDefenseValue = self.get_terrain(attacker.get_row_number(), attacker.get_col_number()).getDefenseBonus()
            attackerDied = defender.standard_attack(attacker, attackerTerrainDefenseValue)

        if attackerDied:
            print("Attacker died")
            self.remove_piece(attacker)
    
    def calc_and_set_postmove_options(self, piece : Piece, movedSameSpot):
        #options = [PostmoveOptions.WAIT]
        postmoveOptionsObject = piece.getPostmoveOptions()
        attackableEnemies = get_pieces_within_range(piece, self) 
        rangedUnitMoved = not movedSameSpot and (piece.get_maxRange() >= 2)
        currentTerrain = self.get_terrain(piece.get_row_number(), piece.get_col_number())
        if currentTerrain.getTerrainName() == BuildingEnums.NAME:
            if currentTerrain.canGetCapturedBy(piece):
                print("Moved footman or archer to building")
                postmoveOptionsObject.appendOption(PostmoveOptionsEnums.CAPTURE)
                postmoveOptionsObject.setBuilding(currentTerrain)
        # TODO eventually abstract all detection methods on determining if an option is available or not
        if (len(attackableEnemies) != 0 and not rangedUnitMoved):
            postmoveOptionsObject.appendOption(PostmoveOptionsEnums.ATTACK)
            postmoveOptionsObject.setAttackableEnemies(attackableEnemies)

    # true if white, false if black
    def whose_turn(self):
        return self.white_turn
    
    def whose_turn_string(self):
        if(self.whose_turn()):
            return Player.PLAYER_1
        else:
            return Player.PLAYER_2

    def is_current_players_piece(self, piece):
        return self.whose_turn() == (piece.get_player() == Player.PLAYER_1)

    def is_current_players_building(self, terrain):
        return self.whose_turn() == (terrain.getOwningPlayer() == Player.PLAYER_1)
    
    def runStartOfTurn(self):
        currentPlayer = self.whose_turn_string()
        self.runStartOfTurnHeal(currentPlayer)
        self.runStartOfTurnFunds(currentPlayer)
    
    def runStartOfTurnHeal(self, currentPlayer):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                terrain = self.get_terrain(r, c)
                if terrain.isBuilding():
                    if terrain.getOwningPlayer() == currentPlayer:
                        piece = self.get_piece(r, c)
                        if piece is not None and piece != Player.EMPTY and piece != Player.WALL:
                            if piece.get_player() == currentPlayer:
                                piece.gainHealth(20)

    def getPlayerBuildingCount(self, player):
        count = 0
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                terrain = self.get_terrain(r, c)
                if terrain.isBuilding():
                    if terrain.getOwningPlayer() == player:
                        count += 1
        return count
    
    def runStartOfTurnFunds(self, currentPlayer):
        count = self.getPlayerBuildingCount(currentPlayer)
        self.playerFunds[currentPlayer] += (count * FundsEnums.IncomePerBuilding)

# TODO: use this later to track moves and have undo or something
# class chess_move():
#     def __init__(self, starting_square, ending_square, game_state):
#         self.starting_square_row = starting_square[0]
#         self.starting_square_col = starting_square[1]
#         self.moving_piece = game_state.get_piece(self.starting_square_row, self.starting_square_col)

#         self.ending_square_row = ending_square[0]
#         self.ending_square_col = ending_square[1]
#         if game_state.is_valid_piece(self.ending_square_row, self.ending_square_col):
#             self.removed_piece = game_state.get_piece(self.ending_square_row, self.ending_square_col)
#         else:
#             self.removed_piece = Player.EMPTY

#         self.knight_starting_square = None
#         self.knight_ending_square = None
#         self.moving_knight = None

#         self.footman_promoted = False
#         self.replacement_piece = None

#     def get_moving_piece(self):
#         return self.moving_piece
