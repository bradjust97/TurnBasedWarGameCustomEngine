# Per-unit movement modifiers override the terrain's default penalty.
# Each modifier maps a terrain name to the penalty for entering that terrain;
# terrains not listed fall back to terrain.getMovementPenalty().
#
# To add a new modifier: add an entry here, then set MOVEMENT_MODIFIER = '<name>'
# on the unit's enum. Units sharing a modifier just point at the same key.
movementModifierPenalties = {
    'foot': {
        'road': 0,
        'plains': 0,
        'forest': 0,
        'mountain': 2,
    },
    'boot': {
        'road': 0,
        'plains': 0,
        'forest': 0,
        'mountain': 0,
        'building': 0,
    },
}
