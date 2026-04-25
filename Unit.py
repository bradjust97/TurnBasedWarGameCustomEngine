import math
import random

from enums import LuckEnums, PostmoveOptionsEnums
from postmoveOptions import postmoveOptions
from combatModifiers import modifierDict


class Unit:
    def __init__(self, name, row_number, col_number, player, movement=0, maxRange=1, minRange=1, health=100):
        self._name = name
        self.row_number = row_number
        self.col_number = col_number
        self._player = player
        self._movement = movement
        self.maxRange = maxRange
        self.minRange = minRange
        self.postmoveActions = [PostmoveOptionsEnums.WAIT, PostmoveOptionsEnums.ATTACK]
        self.postmoveOptions = postmoveOptions()
        self.health = health

    def get_row_number(self):
        return self.row_number

    def get_col_number(self):
        return self.col_number

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

    def get_valid_piece_moves(self, board):
        pass

    def attack_damage(self, target, terrainDefense, luck):
        # AW-style: luck (0..LuckEnums.MAX) is added to the base matchup
        # damage, then the sum is scaled by attacker HP and defender
        # terrain. So weak units can't suddenly do +9% damage.
        attackerHP = self.getHealth() / 10
        attackerModifier = modifierDict[self.get_name()][target.get_name()]
        defenseValue = (200 - 100 - terrainDefense * target.getHealth() / 10) / 100
        return (attackerHP / 10) * (attackerModifier + luck) * defenseValue

    def attack_damage_range(self, target, terrainDefense):
        return (self.attack_damage(target, terrainDefense, LuckEnums.MIN),
                self.attack_damage(target, terrainDefense, LuckEnums.MAX))

    def standard_attack(self, target, terrainDefense=0):
        luck = random.randint(LuckEnums.MIN, LuckEnums.MAX)
        target.loseHealth(self.attack_damage(target, terrainDefense, luck))
        return target.isDead()

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
