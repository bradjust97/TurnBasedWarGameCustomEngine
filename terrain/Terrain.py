class Terrain:
    # Initialize the piece
    def __init__(self, name, row_number, col_number, defenseBonus=0, movementPenalty=0):
        self._name = name
        self.row_number = row_number
        self.col_number = col_number
        self.defenseBonus = defenseBonus
        self.movementPenalty = movementPenalty

    def getTerrainName(self):
        return self._name

    def getRow(self):
        return self.row_number
    
    def getCol(self):
        return self.col_number
    
    def getDefenseBonus(self):
        return self.defenseBonus
    
    def getMovementPenalty(self):
        return self.movementPenalty