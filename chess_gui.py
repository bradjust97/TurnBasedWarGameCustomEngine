from pprint import pprint
import chess_engine
import pygame as py

from enums import Player, SquareBoard

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


def draw_game_state(screen, game_state, valid_moves, square_selected):
    ''' Draw the complete chess board with pieces

    Keyword arguments:
        :param screen       -- the pygame screen
        :param game_state   -- the state of the current chess game
    '''
    draw_squares(screen)
    highlight_square(screen, game_state, valid_moves, square_selected)
    draw_walls(screen, game_state)
    draw_pieces(screen, game_state)
    grayout_squares(screen, game_state)

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

    game_state = chess_engine.game_state()

    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
                if not game_over:
                    location = py.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if square_selected == (row, col):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2:
                        # this if is useless right now
                        if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []
                        else:
                            print("attempting to move piece")
                            game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
                                                  (player_clicks[1][0], player_clicks[1][1]))
                            movedPiece = game_state.get_piece(player_clicks[1][0], player_clicks[1][1])
                            print(movedPiece.get_row_number())
                            print(movedPiece.get_col_number())
                            game_state.get_postmove_options(movedPiece)
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []

                    else:
                        valid_moves = game_state.get_valid_moves((row, col))
                        if valid_moves is None:
                            print("valid moves is none")
                            valid_moves = []
            elif e.type == py.KEYDOWN:
                if (e.key == py.K_e):
                    print("End turn pressed")
                    game_state.end_turn()
                    game_state.reset_moved_pieces()
                # if e.key == py.K_r:
                #     game_over = False
                #     game_state = chess_engine.game_state()
                #     valid_moves = []
                #     square_selected = ()
                #     player_clicks = []
                #     valid_moves = []
                # elif e.key == py.K_u:
                #     game_state.undo_move()
                #     print(len(game_state.move_log))

        draw_game_state(screen, game_state, valid_moves, square_selected)

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


if __name__ == "__main__":
    main()
