#
# The piece classes
#
# TODO: add checking if check after moving suggested move later

# General piece
import math
from enums import Player, PostmoveOptionsEnums, SquareBoard
from postmoveOptions import postmoveOptions
from combatModifiers import modifierDict


class Piece:
    # Initialize the piece
    def __init__(self, name, row_number, col_number, player, movement=0, maxRange=1, minRange=1, health=100):
        self._name = name
        self.row_number = row_number
        self.col_number = col_number
        self._player = player
        self._movement = movement
        self.maxRange = maxRange
        self.minRange = minRange
        # For now assume every piece can either wait or attack. TODO change this to inherit
        self.postmoveActions = [PostmoveOptionsEnums.WAIT, PostmoveOptionsEnums.ATTACK]
        self.postmoveOptions = postmoveOptions()
        self.health = health

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

    def get_movement(self):
        return self._movement

    def get_maxRange(self):
        return self.maxRange
    
    def get_minRange(self):
        return self.minRange

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

    def standard_attack(self, target, terrainDefense=0):
        killTarget = False
        print("_____________________")
        print("Attacking target")
        attackerHP = self.getHealth() / 10
        print("hp of attacker")
        print(attackerHP)
        attackerModifier = modifierDict[self.get_name()][target.get_name()]
        print("terrainDefense")
        print(terrainDefense)
        print("starting hp of attacker")
        print(attackerHP)
        print("starting hp of defender")
        print(target.getHealth() / 10)
        defenseValue = (200 - 100 - terrainDefense * target.getHealth() / 10) / 100
        print("defenseValue")
        print(defenseValue)
        print("attackerModifier")
        print(attackerModifier)
        hpLoss = (attackerHP / 10) * attackerModifier * defenseValue
        print("hpLoss")
        print(hpLoss)
        target.loseHealth(hpLoss)
        print("Target is at hp:" + str(target.getHealth()))
        print("_____________________")
        if target.isDead(): 
            killTarget = True
        return killTarget

    
    def getPostmoveActions(self):
        return self.postmoveActions

    def getPostmoveOptions(self):
        return self.postmoveOptions

    def resetPostmoveOptions(self):
        self.postmoveOptions.resetOptions()
    
    def getHealth(self):
        return self.health
    
    def getHP(self):
        return math.ceil(self.health / 10)
    
    def loseHealth(self, hp):
        self.health -= hp
    
    def gainHealth(self, hp):
        self.health += hp
        if self.health > 100:
            self.health = 100
    
    def isDead(self):
        return self.health <= 0

    def isAlive(self):
        return not self.isDead()










