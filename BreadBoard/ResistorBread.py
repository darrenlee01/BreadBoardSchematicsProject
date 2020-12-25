#Sub class of DeviceBread, defines a new Breadboard Resistor

from DeviceBread import *
import sys # Following code from sys
#learned to use sys from Stack Overflow
#https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
sys.path.append("Devices")

from Resistor import *
class ResistorBread(DeviceBread):

    scale = 0.25
    cropDim = None
    height = 70
    
    url = "Resistor Bread Board.PNG" #self-made vector image
    def __init__(self, n1x, n1y, n2x, n2y, resistance, isWire = False):
        if (not isWire):
            super().__init__(ResistorBread.url, ResistorBread.scale, 
                                        n1x, n1y, n2x, n2y)
        else:
            super().__init__(None, None, n1x, n1y, n2x, n2y)

        self.resistance = resistance

    def __repr__(self):
        return str(self.resistance) + " Resistor - " + str(self.n1.occupyingHole) + "& " + str(self.n2.occupyingHole)

    def toDevice(self, leftDevice, rightDevice):
        deviceForm = Resistor(leftDevice, rightDevice, self.resistance)
        return deviceForm
    
    def getResistance(self):
        return self.resistance

