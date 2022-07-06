import enum
import math
from pprint import pprint
from units.Footman import Footman
from Piece import Piece
import chess_engine
import pygame as py
from combat_engine import get_pieces_within_range

from enums import Player, PostmoveOptionsEnums, SquareBoard, TerrainEnums

"""Variables"""
WIDTH = SquareBoard.WIDTH  # width and height of the chess board
HEIGHT = SquareBoard.HEIGHT
DIMENSION = SquareBoard.DIMENSIONS  # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the chess pieces
colors = [py.Color("white"), py.Color("gray"), py.Color("black")]
TERRAINIMAGES = {}

def load_images():
    '''
    Load images for the chess pieces
    '''
    for p in Player.PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))
    for u in Player.UNITS:
        IMAGES[u] = py.transform.scale(py.image.load("images/advancedWars/" + u + ".png"), (SQ_SIZE, SQ_SIZE))
    for tName in TerrainEnums.TYPES:
        TERRAINIMAGES[tName] = py.transform.scale(py.image.load("images/terrain/" + tName + ".png"), (SQ_SIZE, SQ_SIZE))

def draw_game_state(screen, game_state, valid_moves, square_selected, currentAttackableEnemies):
    ''' Draw the complete chess board with pieces

    Keyword arguments:
        :param screen       -- the pygame screen
        :param game_state   -- the state of the current chess game
    '''
    # print("drawing new game state")
    # print(square_selected)
    # if len(square_selected) == 2:
    #     print(game_state.get_piece(square_selected[0], square_selected[1]))
    # square selected and game state appear to have the knight but it still doesnt show up
    draw_squares(screen)
    draw_walls(screen, game_state)
    draw_terrain(screen, game_state)
    if (square_selected != None):
        highlight_square(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state)
    draw_unit_healths(screen, game_state)
    grayout_squares(screen, game_state)
    redden_squares(screen, currentAttackableEnemies)

def draw_walls(screen, game_state):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece == Player.WALL:
                py.draw.rect(screen, colors[2], py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_squares(screen):
    ''' Draw the chess board with the alternating two colors

    :param screen:          -- the pygame screen
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            py.draw.rect(screen, color, py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_terrain(screen, game_state):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            terrain = game_state.get_terrain(r, c)
            if terrain is not None:
                screen.blit(TERRAINIMAGES[terrain.getTerrain()],
                            py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, game_state):
    ''' Draw the chess pieces onto the board

    :param screen:          -- the pygame screen
    :param game_state:      -- the current state of the chess game
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY and piece != Player.WALL:
                screen.blit(IMAGES[piece.get_player() + "_" + piece.get_name()],
                            py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_square(screen, game_state, valid_moves, square_selected):
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]) and \
        not game_state.has_piece_moved(game_state.get_piece(square_selected[0], square_selected[1])):

        row = square_selected[0]
        col = square_selected[1]

        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_1)) or \
                (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_2)):
            # hightlight selected square
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(py.Color("blue"))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

            # highlight move squares
            s.fill(py.Color("green"))

            for move in valid_moves:
                screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))
    
def grayout_squares(screen, game_state):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY and piece != Player.WALL and game_state.has_piece_moved(piece):
                s = py.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)
                s.fill(py.Color("grey"))
                screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

def redden_squares(screen, pieces):
    for piece in pieces:
        r = piece.get_row_number()
        c = piece.get_col_number()
        s = py.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(py.Color("red"))
        screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
    # for r in range(DIMENSION):
    #     for c in range(DIMENSION):
    #         piece = game_state.get_piece(r, c)
    #         if piece is not None and piece != Player.EMPTY and piece != Player.WALL and game_state.has_piece_moved(piece):
    #             s = py.Surface((SQ_SIZE, SQ_SIZE))
    #             s.set_alpha(100)
    #             s.fill(py.Color("grey"))
    #             screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


def main():
    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    game_state = chess_engine.game_state()
    load_images()
    running = True
    square_selected = ()  # keeps track of the last selected square
    player_clicks = []  # keeps track of player clicks (two tuples)
    valid_moves = []
    game_over = False
    pieceIsSelected = False
    continuePostmove = False
    currentAttackableEnemies = []
    godmode = False

    game_state = chess_engine.game_state()

    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
            # -----------------------------------------------------------
                if godmode:
                    location = py.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    footman = Footman(row, col, Player.PLAYER_1)
                    # TODO this should really have its own method
                    game_state.board[row][col] = footman
                elif not game_over:
                    location = py.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if not pieceIsSelected:
                        if game_state.is_valid_piece(row, col):
                            potentialPiece = game_state.get_piece(row, col)
                            if (not game_state.has_piece_moved(potentialPiece) and game_state.is_current_players_piece(potentialPiece)):
                                print ("selected valid piece")
                                square_selected = (row, col)
                                player_clicks.append(square_selected)
                                valid_moves = game_state.get_valid_moves((row, col))
                                pieceIsSelected = True
                                if valid_moves is None:
                                    print("valid moves is none")
                                    valid_moves = []
                                    player_clicks = []
                                    square_selected = ()
                                    pieceIsSelected = False
                                else: 
                                    print("valid moves exist")
                            else: 
                                print("piece has already moved or that is an enemy unit")
                                square_selected = ()
                                player_clicks = []
                                valid_moves = [] #TODO This may be a bug to add this line double check this
                                pieceIsSelected = False
                        else:
                            print("not a valid piece")
                            square_selected = ()
                            player_clicks = []
                            valid_moves = [] #TODO This may be a bug to add this line double check this
                            pieceIsSelected = False
                    elif pieceIsSelected:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                        if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
                            # reset the piece selected
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []
                            pieceIsSelected = False
                            print("Out of movement range")
                        elif continuePostmove:
                            # TODO this needs to be extracted for different moves
                            finishedOption = execute_selected_option(game_state, movedPiece, square_selected)
                            if (finishedOption):
                                square_selected = ()
                                player_clicks = []
                                valid_moves = []
                                pieceIsSelected = False
                                continuePostmove = False
                                currentAttackableEnemies = []
                            else:
                                print("please select valid postmove attack")
                        else:
                            # move piece and do postmove stuff, then reset
                            (movedPiece, movedSameSpot) = gui_move(game_state, player_clicks)
                            game_state.calc_and_set_postmove_options(movedPiece, movedSameSpot)
                            continuePostmove = movedPiece.getPostmoveOptions().hasAttackOption()
                            # if piece has no options then just end the piece movement and reset
                            if not continuePostmove:
                                square_selected = ()
                                player_clicks = []
                                valid_moves = []
                                pieceIsSelected = False
                            # setup gui for user input post move
                            else:
                                currentAttackableEnemies = movedPiece.getPostmoveOptions().getAttackableEnemies()
            # --------------------------------------------------------
            elif e.type == py.KEYDOWN:
                if (e.key == py.K_e):
                    print("End turn pressed")
                    square_selected = ()
                    player_clicks = []
                    valid_moves = []
                    pieceIsSelected = False
                    continuePostmove = False
                    currentAttackableEnemies = []
                    game_state.end_turn()
                    game_state.reset_moved_pieces()
                elif (e.key == py.K_g):
                    godmode = not godmode
                    if godmode:
                        print("WARNING: GODMODE ENABLED")
                    else:
                        print("godmode disabled, phew...")
                # debug function
                elif (e.key == py.K_x):
                    print("x")
                    # font = py.font.SysFont("Helvitca", 32, True, False)
                    # text_object = font.render("1", False, py.Color("Red"))
                    # text_location = py.Rect(0, 0, WIDTH, HEIGHT).move(5,5)
                    # screen.blit(text_object, text_location)

                    
        draw_game_state(screen, game_state, valid_moves, square_selected, currentAttackableEnemies)

        endgame = game_state.isDeadKing()
        if endgame == 0 or game_over:
            game_over = True
            draw_text(screen, "Black wins.")
        elif endgame == 1 or game_over:
            game_over = True
            draw_text(screen, "White wins.")
        elif endgame == 2 or game_over:
            game_over = True
            draw_text(screen, "Stalemate.")

        clock.tick(MAX_FPS)
        py.display.flip()

def draw_text(screen, text):
    font = py.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, False, py.Color("Red"))
    text_location = py.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                      HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)

def draw_unit_healths(screen, game_state):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY and piece != Player.WALL:
                hp = piece.getHealth()
                if  hp < 100:
                    # TODO 512 is the width and height and scale it based on board BITCH
                    centerOfGridLocationByPixelRow = ((SquareBoard.WIDTH / SquareBoard.DIMENSIONS) * (r+1)) - ((SquareBoard.WIDTH / SquareBoard.DIMENSIONS) / 2) - 1
                    centerOfGridLocationByPixelCol = ((SquareBoard.WIDTH / SquareBoard.DIMENSIONS) * (c+1)) - ((SquareBoard.WIDTH / SquareBoard.DIMENSIONS) / 2) - 1

                    # This is a shitshow but allow me to explain my logic. W / D signifies the amount of pixels a grid space takes up
                    # So take that and multiply it by the row we are looking at. The +1 is because we are indexed at 0. The next W/2D 
                    # is because we want the top left of the image to be in the center of the grid space. The - 1 puts us at exactly the center 
                    # because 0 index. Lastly below we have col row because the x y is swapped due to error. Ideally we should change everything
                    # to be consistent but for now this is what it is
                    pixelLocation = (centerOfGridLocationByPixelCol, centerOfGridLocationByPixelRow )
                    font = py.font.SysFont("Helvitca", 32, True, False)
                    hp = hp / 10
                    hpText = str(math.floor(hp))
                    text_object = font.render(hpText, True, py.Color("Green")) 
                    screen.blit(text_object, pixelLocation)

def processOptions(options):
    # if 0 in options:
    #     text = "What would you like to do? 0 = wait\n"
    # if 1 in options:
    #     text = "What would you like to do? 0 = wait 1 = attack\n"
    # return text
    return "What would you like to do? 0 = wait 1 = attack\n"

def gui_move(game_state, player_clicks):
    movedSameSpot = game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
    (player_clicks[1][0], player_clicks[1][1]))
    movedPiece = game_state.get_piece(player_clicks[1][0], player_clicks[1][1])
    print(movedPiece)
    return (movedPiece, movedSameSpot)

def execute_selected_option(game_state: chess_engine.game_state, sourcePiece: Piece, selected_square):
    # return true if successfully executed option
    # TODO this is only for attack, need to generalize for multiple options
    attack = True
    if (attack):
        attackablePieces = sourcePiece.getPostmoveOptions().getAttackableEnemies()
        if game_state.is_valid_piece(selected_square[0], selected_square[1]):
            target = game_state.get_piece(selected_square[0], selected_square[1])   
            if target in attackablePieces:
                game_state.attack_piece(sourcePiece, target)
                sourcePiece.getPostmoveOptions().resetOptions()
                return True
            else:
                print("not a valid piece to attack")
                return False
        else:
            print("not a valid square to attack")


if __name__ == "__main__":
    main()
