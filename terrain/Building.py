

from Piece import Piece
from enums import ArcherEnums, BuildingEnums, FootmanEnums
from terrain.Terrain import Terrain


class Building(Terrain):
    def __init__(self, row_number, col_number, player=None):
        self.owningPlayer = player
        self.currentCapturePoints = BuildingEnums.TOTALCAPTUREPOINTS

        name = BuildingEnums.NAME
        defenseBonus = BuildingEnums.DEFENSEBONUS
        movementPenalty = BuildingEnums.MOVEMENTPENALTY
        super().__init__(name, row_number, col_number, defenseBonus, movementPenalty)
    
    def getOwningPlayer(self):
        return self.owningPlayer
    
    def setOwningPlayer(self, player):
        self.owningPlayer = player
    
    def getCapturePoints(self):
        return self.currentCapturePoints

    def resetCapturePoints(self):
        self.currentCapturePoints = BuildingEnums.TOTALCAPTUREPOINTS
    
    def decrCapturePoints(self, points):
        self.currentCapturePoints -= points
    
    def canCapture(self, piece:Piece):
        if piece.get_name() == FootmanEnums.NAME or piece.get_name() == ArcherEnums.NAME:
            return True
        else:
            return False

    def capture(self, piece:Piece):
        # Returns true if piece successfully captured the building
        if(self.canCapture(piece)):
            self.decrCapturePoints(piece.getHP())
            if self.getCapturePoints <= 0:
                print("Building successfully captured")
                self.setOwningPlayer(piece.get_player())
                return True
            else:
                return False
        else:
            return False
    
