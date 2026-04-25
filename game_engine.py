import math

from Unit import Unit
from combat_engine import get_pieces_within_range
from enums import ArcherEnums, DIMENSION, BuildingEnums, FootmanEnums, FundsEnums, Player, PostmoveOptionsEnums, SquareBoard, TerrainEnums
from startingBoards.defaultBoard import defaultBoard
from terrain.Building import Building
from unitCosts import groundUnitCosts
from units.Archer import Archer
from units.Footman import Footman


BUYABLE_UNIT_NAMES = [FootmanEnums.NAME, ArcherEnums.NAME]
UNIT_FACTORIES = {
    FootmanEnums.NAME: Footman,
    ArcherEnums.NAME: Archer,
}


class game_state:
    def __init__(self):
        self.move_log = []
        self.white_turn = True
        self.white_is_dead = False
        self.black_is_dead = False

        self._white_king_location = [0, 3]
        self._black_king_location = [7, 3]

        self.board = defaultBoard.board
        self.terrain = defaultBoard.terrain
        self.moved_pieces = []
        self.numBlackPieces = len(defaultBoard.black_pieces)
        self.numWhitePieces = len(defaultBoard.white_pieces)
        self.playerFunds = {Player.PLAYER_1: 0, Player.PLAYER_2: 0}

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
            return abs(c1 - c2) == 1
        if c1 == c2:
            return abs(r1 - r2) == 1
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
    
    def remove_piece(self, piece : Unit):
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
    
    def piece_moved(self, piece: Unit):
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

                if temp:
                    moving_piece.change_row_number(next_square_row)
                    moving_piece.change_col_number(next_square_col)
                    self.board[next_square_row][next_square_col] = self.board[current_square_row][current_square_col]
                    self.board[current_square_row][current_square_col] = Player.EMPTY

                self.piece_moved(moving_piece)
                return False
            else:
                return False
    
    def attack_piece(self, attacker: Unit, defender: Unit):
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
    
    def calc_and_set_postmove_options(self, piece : Unit, movedSameSpot):
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
        return self.whose_turn() == (terrain.getOwningPlayer() == Player.PLAYER_1) and terrain.getOwningPlayer() != Player.NEUTRAL
    
    def runStartOfTurn(self):
        currentPlayer = self.whose_turn_string()
        self.runStartOfTurnBuildings()
        self.runStartOfTurnFunds(currentPlayer)
        self.runStartOfTurnHeal(currentPlayer)

    def runStartOfTurnBuildings(self):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                terrain = self.get_terrain(r, c)
                if terrain.isBuilding():
                    terrain.resetTurnState()

    def runStartOfTurnHeal(self, currentPlayer):
        # Heal each friendly unit standing on an owned building, paying
        # 10% of unit cost per HP healed (max 2 HP, capped at full health).
        # Iterate north-to-south, then west-to-east, so northern/western
        # units get priority when funds run short.
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                terrain = self.get_terrain(r, c)
                if not terrain.isBuilding():
                    continue
                if terrain.getOwningPlayer() != currentPlayer:
                    continue
                piece = self.get_piece(r, c)
                if piece is None or piece == Player.EMPTY or piece == Player.WALL:
                    continue
                if piece.get_player() != currentPlayer:
                    continue
                unitCost = groundUnitCosts.get(piece.get_name())
                if unitCost is None:
                    continue
                missingHp = 10 - math.ceil(piece.getHealth() / 10)
                if missingHp <= 0:
                    continue
                costPerHp = unitCost // 10
                if costPerHp <= 0:
                    continue
                affordableHp = min(2, missingHp, self.playerFunds[currentPlayer] // costPerHp)
                if affordableHp <= 0:
                    continue
                piece.gainHealth(affordableHp * 10)
                self.playerFunds[currentPlayer] -= affordableHp * costPerHp

    def getPlayerBuildingCount(self, player):
        count = 0
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                terrain = self.get_terrain(r, c)
                if terrain.isBuilding():
                    if terrain.getOwningPlayer() == player:
                        count += 1
        return count
    
    def getFundsForPlayer(self, player):
        return self.playerFunds[player]
    
    def runStartOfTurnFunds(self, currentPlayer):
        count = self.getPlayerBuildingCount(currentPlayer)
        self.playerFunds[currentPlayer] += (count * FundsEnums.IncomePerBuilding)
    
    def getPossibleBuildGroundUnitsOfCurrentPlayer(self):
        return list(BUYABLE_UNIT_NAMES)

    def canAfford(self, player, unitName):
        cost = groundUnitCosts.get(unitName)
        return cost is not None and self.getFundsForPlayer(player) >= cost

    def buyUnit(self, unitName, row, col):
        if unitName not in UNIT_FACTORIES:
            print("Unit " + str(unitName) + " is not buyable")
            return False
        terrain = self.get_terrain(row, col)
        if terrain is None or not terrain.isBuilding():
            print("No building at that square")
            return False
        currentPlayer = self.whose_turn_string()
        if terrain.getOwningPlayer() != currentPlayer:
            print("Building is not owned by current player")
            return False
        if terrain.producedThisTurn:
            print("Building already produced this turn")
            return False
        if not self.is_empty(row, col):
            print("Building is occupied, cannot spawn unit")
            return False
        cost = groundUnitCosts[unitName]
        if self.playerFunds[currentPlayer] < cost:
            print("Cannot afford " + unitName)
            return False

        self.playerFunds[currentPlayer] -= cost
        newUnit = UNIT_FACTORIES[unitName](row, col, currentPlayer)
        self.board[row][col] = newUnit
        self.incrPieces(currentPlayer)
        self.piece_moved(newUnit)
        terrain.producedThisTurn = True
        print("Bought " + unitName + " at (" + str(row) + "," + str(col) + ")")
        return True
