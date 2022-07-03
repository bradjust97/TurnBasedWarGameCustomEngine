class Player:
    PLAYER_1 = 'white'
    PLAYER_2 = 'black'
    EMPTY = -9
    WALL = -8
    PIECES = ['white_r', 'white_n', 'white_q', 'white_k', 'white_p',
              'black_r', 'black_n', 'black_q', 'black_k', 'black_p']
    UNITS = ['white_scoutCavalry', 'black_scoutCavalry', 'black_knight', 'white_knight',
             'white_footman', 'black_footman', 'white_king', 'black_king', 
             'white_queen', 'black_queen', 'white_catapult', 'black_catapult']
             # No images for:
             # 'white_archer', 'black_archer', and more


class SquareBoard: # assume square for now
    DIMENSIONS = 16
    WIDTH = 512
    HEIGHT = 512

class KingEnums:
    MOVEMENT = 1
    NAME = 'king'

class KnightEnums:
    MOVEMENT = 6
    NAME = 'knight'

class ScoutCavalryEnums:
    MOVEMENT = 8
    NAME = 'scoutCavalry'

class CatapultEnums:
    MOVEMENT = 4
    NAME = 'catapult' 
    MAXRANGE = 4
    MINRANGE = 2

class FootmanEnums:
    MOVEMENT = 3
    NAME = 'footman'

class ArcherEnums:
    MOVEMENT = 2
    NAME = 'archer'

class WagonerEnums:
    MOVEMENT = 5
    NAME = 'wagoner'

class LancerEnums:
    MOVEMENT = 7
    NAME = 'lancer'

class NobleEnums:
    MOVEMENT = 9
    NAME = 'noble'

class TrebuchetEnums:
    MOVEMENT = 7
    NAME = 'trebuchet'

class BallistaEnums:
    MOVEMENT = 7
    NAME = 'ballista'

class HuntsmanEnums:
    MOVEMENT = 7
    NAME = 'huntsman'

class WarWagonEnums:
    MOVEMENT = 7
    NAME = 'warWagon'

class PostmoveOptionsEnums:
    WAIT = 0
    ATTACK = 1
    WAITORATTACKTEXT = "What would you like to do? 0 = wait 1 = attack\n"

