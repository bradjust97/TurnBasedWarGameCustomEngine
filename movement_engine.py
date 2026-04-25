import heapq

from movementModifiers import movementModifierPenalties


def _step_cost(terrain, movement_modifier):
    overrides = movementModifierPenalties.get(movement_modifier)
    if overrides is not None and terrain.getTerrainName() in overrides:
        return overrides[terrain.getTerrainName()] + 1
    return terrain.getMovementPenalty() + 1


def blocked_movement_diamond(movement, row_number, col_number, game_state, movement_modifier=None):
    """All squares reachable from (row, col) within `movement` cost.

    Cost to enter a tile = terrain.getMovementPenalty() + 1, unless the unit
    has a movement_modifier that overrides the penalty for that terrain.
    The origin is free (cost 0) and always included — this supports "click
    self to wait". Any occupied tile (friendly, enemy, or wall) blocks
    traversal; swap the is_empty check for an enemy-only check if you want
    friendlies to be pass-through.
    """
    origin = (row_number, col_number)
    best_cost = {origin: 0}
    frontier = [(0, row_number, col_number)]

    while frontier:
        cost, r, c = heapq.heappop(frontier)
        if cost > best_cost[(r, c)]:
            continue
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if not game_state.is_empty(nr, nc):
                continue
            step_cost = _step_cost(game_state.get_terrain(nr, nc), movement_modifier)
            new_cost = cost + step_cost
            if new_cost > movement:
                continue
            if new_cost < best_cost.get((nr, nc), float('inf')):
                best_cost[(nr, nc)] = new_cost
                heapq.heappush(frontier, (new_cost, nr, nc))

    return list(best_cost.keys())
