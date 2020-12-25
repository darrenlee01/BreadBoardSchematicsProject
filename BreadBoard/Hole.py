#class for the holes on the breadboard

class Hole():
    def __init__(self, x, y, r = None, c = None, isMainBoard = 0):
        self.x = x
        self.y = y
        self.row = r
        self.col = c
        self.removeOccupied()
        self.isMainBoard = isMainBoard
    
    def __repr__(self):
        if (self.row != None and self.col != None):
            return "Hole - (" + str(self.row) + ", " + str(self.col) + ") "
        else:
            if (self.isMainBoard > 0):
                return "Pos Rail Hole"
            else:
                return "Neg Rail Hole"
    
    def removeOccupied(self):
        self.occupyingNode = None
        self.occupyingDevice = None
