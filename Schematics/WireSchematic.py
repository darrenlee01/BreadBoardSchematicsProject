#Sub class of ResistorSchematic, defines a Schematic Wire

from ResistorSchematic import *
class WireSchematic(ResistorSchematic):
    #will just draw a line
    height = 10

    def __init__(self, n1x, n1y, n2x, n2y):
        super().__init__(n1x, n1y, n2x, n2y, 0, isWire = True)

    def __repr__(self):
        return "Wire - (" + str(self.cx) + ", " + str(self.cy) + ")"