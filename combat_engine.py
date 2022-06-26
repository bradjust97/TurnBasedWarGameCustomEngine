import itertools

from enums import Player


def get_pieces_within_range(piece, game_state):
    row_change = list(range(piece.get_range() * -1, piece.get_range() + 1))
    col_change = list(range(piece.get_range() * -1, piece.get_range() + 1))
    square = list(itertools.product(row_change, col_change))
    diamond = []
    attackableEnemyPieces = []
    for move in square:
        # restrict movement with no diags
        if (abs(move[0]) + abs(move[1])) <= piece.get_range():
            diamond.append(move)

    for i in range(0, len(diamond)):
            new_row = piece.get_row_number() + diamond[i][0]
            new_col = piece.get_col_number() + diamond[i][1]
            # when the square with new_row and new_col contains a valid piece
            if (game_state.is_valid_piece(new_row, new_col)):
                potentialPiece = game_state.get_piece(new_row, new_col)
                whiteTurn = game_state.whose_turn()
                whitePiece = potentialPiece.get_player() == Player.PLAYER_1
                # if its both a white piece and the white turn, then its friendly
                # if its both a black piece and the black turn, then its friendly
                isFriendly = whiteTurn == whitePiece
                if not isFriendly and game_state:
                    attackableEnemyPieces.append(potentialPiece)
                    # # when the king is white and the piece near the king is black
                    # if piece.is_player(Player.PLAYER_1) and evaluating_square.is_player(Player.PLAYER_2):
                    #     _moves.append((new_row, new_col))
                    # # when the king is black and the piece near the king is white
                    # elif piece.is_player(Player.PLAYER_2) and evaluating_square.is_player(Player.PLAYER_1):
                    #     _moves.append((new_row, new_col))
    return attackableEnemyPieces

# def attack(attacking_piece, target):