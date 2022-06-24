class Player:
    PLAYER_1 = 'white'
    PLAYER_2 = 'black'
    EMPTY = -9
    PIECES = ['white_r', 'white_n', 'white_q', 'white_k', 'white_p',
              'black_r', 'black_n', 'black_q', 'black_k', 'black_p']
    UNITS = ['white_recon', 'black_recon', 'black_tank', 'white_infantry', 'black_infantry', 'white_king', 'white_queen','black_king', 'black_queen', 'white_tank', 'black_tank', 'white_artillery', 'black_artillery']


class SquareBoard: # assume square for now
    DIMENSIONS = 16
    WIDTH = 512
    HEIGHT = 512

class KingEnums:
    MOVEMENT = 1
    NAME = 'king'

class QueenEnums:
    MOVEMENT = 1
    NAME = 'queen'

class RookEnums:
    MOVEMENT = 1
    NAME = 'tank'

class BishopEnums:
    MOVEMENT = 1
    NAME = 'recon'

class KnightEnums:
    MOVEMENT = 1
    NAME = 'artillery' 

class PawnEnums:
    MOVEMENT = 1
    NAME = 'infantry'