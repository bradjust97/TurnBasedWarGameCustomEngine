import enum
from pprint import pprint
from Piece import Piece
import chess_engine
import pygame as py
from combat_engine import get_pieces_within_range

from enums import Player, PostmoveOptionsEnums, SquareBoard

"""Variables"""
WIDTH = SquareBoard.WIDTH  # width and height of the chess board
HEIGHT = SquareBoard.HEIGHT
DIMENSION = SquareBoard.DIMENSIONS  # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the chess pieces
colors = [py.Color("white"), py.Color("gray"), py.Color("black")]

def load_images():
    '''
    Load images for the chess pieces
    '''
    for p in Player.PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))
    for u in Player.UNITS:
        IMAGES[u] = py.transform.scale(py.image.load("images/advancedWars/" + u + ".png"), (SQ_SIZE, SQ_SIZE))


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
    if (square_selected != None):
        highlight_square(screen, game_state, valid_moves, square_selected)
    draw_walls(screen, game_state)
    draw_pieces(screen, game_state)
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

    game_state = chess_engine.game_state()

    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
            # -----------------------------------------------------------
                if not game_over:
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
                            # todo make clicking for wait actionable? or just auto resolve if only option is wait. will prob need this when selecting unit
                            movedPiece = gui_move(game_state, player_clicks)
                            # draw_game_state(screen, game_state, valid_moves, square_selected)
                            # py.display.flip()
                            game_state.calc_and_set_postmove_options(movedPiece)
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
                    game_state.end_turn()
                    game_state.reset_moved_pieces()
                    
        draw_game_state(screen, game_state, valid_moves, square_selected, currentAttackableEnemies)

        # endgame = game_state.checkmate_stalemate_checker()
        endgame = game_state.isDeadKing()
        if endgame == 0:
            game_over = True
            draw_text(screen, "Black wins.")
        elif endgame == 1:
            game_over = True
            draw_text(screen, "White wins.")
        elif endgame == 2:
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

def processOptions(options):
    # if 0 in options:
    #     text = "What would you like to do? 0 = wait\n"
    # if 1 in options:
    #     text = "What would you like to do? 0 = wait 1 = attack\n"
    # return text
    return "What would you like to do? 0 = wait 1 = attack\n"

def gui_move(game_state, player_clicks):
    game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
    (player_clicks[1][0], player_clicks[1][1]))
    movedPiece = game_state.get_piece(player_clicks[1][0], player_clicks[1][1])
    print(movedPiece)
    return movedPiece

def execute_selected_option(game_state, sourcePiece: Piece, selected_square):
    # return true if successfully executed option
    # TODO this is only for attack, need to generalize for multiple options
    attack = True
    if (attack):
        attackablePieces = sourcePiece.getPostmoveOptions().getAttackableEnemies()
        if game_state.is_valid_piece(selected_square[0], selected_square[1]):
            target = game_state.get_piece(selected_square[0], selected_square[1])   
            if target in attackablePieces:
                targetKilled = sourcePiece.standard_attack(target)
                if targetKilled:
                    game_state.remove_piece(target)
                sourcePiece.getPostmoveOptions().resetOptions()
                return True
            else:
                print("not a valid piece to attack")
                return False
        else:
            print("not a valid square to attack")


if __name__ == "__main__":
    main()
