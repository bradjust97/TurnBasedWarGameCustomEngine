class Player:
    PLAYER_1 = 'white'
    PLAYER_2 = 'black'
    NEUTRAL = 'neutral'
    EMPTY = -9
    WALL = -8
    UNITS = ['white_scoutCavalry', 'black_scoutCavalry', 'black_knight', 'white_knight',
             'white_footman', 'black_footman', 'white_king', 'black_king',
             'white_queen', 'black_queen', 'white_catapult', 'black_catapult', 'white_archer', 'black_archer']


class SquareBoard: # assume square for now
    DIMENSIONS = 16
    WIDTH = 512
    HEIGHT = 512

class SideMenu:
    WIDTH = 256
    HEIGHT = SquareBoard.HEIGHT

class BottomMenu:
    WIDTH = SquareBoard.WIDTH
    HEIGHT = 128

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
    MOVEMENT_MODIFIER = 'foot'

class ArcherEnums:
    MOVEMENT = 2
    NAME = 'archer'
    MOVEMENT_MODIFIER = 'boot'

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
    CAPTURE = 2
    WAITORATTACKTEXT = "What would you like to do? 0 = wait 1 = attack\n"

class RoadEnums:
    NAME = 'road'
    DEFENSEBONUS = 0
    MOVEMENTPENALTY = 0

class PlainsEnums:
    NAME = 'plains'
    DEFENSEBONUS = 1
    MOVEMENTPENALTY = 0

class ForestEnums:
    NAME = 'forest'
    DEFENSEBONUS = 2
    MOVEMENTPENALTY = 1

class MountainEnums:
    NAME = 'mountain'
    DEFENSEBONUS = 4
    MOVEMENTPENALTY = 2

class BuildingEnums:
    NAME = 'building'
    DEFENSEBONUS = 3
    MOVEMENTPENALTY = 0
    TOTALCAPTUREPOINTS = 20

class TerrainEnums:
    TYPES = [RoadEnums.NAME, 
            PlainsEnums.NAME, 
            ForestEnums.NAME, 
            MountainEnums.NAME, 
            Player.PLAYER_1 + '_' + BuildingEnums.NAME, 
            Player.PLAYER_2 + '_' + BuildingEnums.NAME,
            Player.NEUTRAL + '_' + BuildingEnums.NAME]
    ROAD = RoadEnums
    PLAINS = PlainsEnums
    FOREST = ForestEnums
    MOUNTAIN = MountainEnums
    BUILDING = BuildingEnums

class FundsEnums:
    IncomePerBuilding = 1000

class LuckEnums:
    MIN = 0
    MAX = 9


"""Variables"""
WIDTH = SquareBoard.WIDTH  # width and height of the board
HEIGHT = SquareBoard.HEIGHT
SIDEMENUWIDTH = SideMenu.WIDTH
SIDEMENUHEIGHT = SideMenu.HEIGHT + BottomMenu.HEIGHT
BOTTOMMENUWIDTH = BottomMenu.WIDTH + SideMenu.WIDTH
BOTTOMMENUHEIGHT = BottomMenu.HEIGHT
DIMENSION = SquareBoard.DIMENSIONS  # the dimensions of the board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the pieces
TERRAINIMAGES = {}