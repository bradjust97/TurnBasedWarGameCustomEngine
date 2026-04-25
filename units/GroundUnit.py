from Unit import Unit
from movement_engine import blocked_movement_diamond


class GroundUnit(Unit):
    enums = None

    def __init__(self, row_number, col_number, player):
        e = self.enums
        super().__init__(
            e.NAME,
            row_number,
            col_number,
            player,
            e.MOVEMENT,
            getattr(e, 'MAXRANGE', 1),
            getattr(e, 'MINRANGE', 1),
        )

    def get_valid_piece_moves(self, game_state):
        return blocked_movement_diamond(
            self.enums.MOVEMENT,
            self.get_row_number(),
            self.get_col_number(),
            game_state,
            getattr(self.enums, 'MOVEMENT_MODIFIER', None),
        )
