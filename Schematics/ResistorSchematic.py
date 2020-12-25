#Sub class of DeviceSchematic, defines a Schematic Resistor

from DeviceSchematic import *
import sys # Following code from sys
sys.path.append("Devices")
#learned to use sys from Stack Overflow
#https://stackoverflow.com/questions/4383571/importing-files-from-different-folder

from Resistor import *
class ResistorSchematic(DeviceSchematic):

    scale = 0.7 #need to adjust
    cropDim = None
    height = 120
    
    url = "Resistor.PNG" #self-made vector image
    def __init__(self, n1x, n1y, n2x, n2y, resistance, isWire = False):
        if (not isWire):
            super().__init__(ResistorSchematic.url, ResistorSchematic.scale, 
                                        n1x, n1y, n2x, n2y)
        else:
            super().__init__(None, None, n1x, n1y, n2x, n2y)

        self.resistance = resistance

    def __repr__(self):
        return str(self.resistance) + " Resistor - (" + str(self.cx) + ", " + str(self.cy) + ")"

    def toDevice(self, leftDevice, rightDevice):
        deviceForm = Resistor(leftDevice, rightDevice, self.resistance)
        return deviceForm
    
    def getResistance(self):
        return self.resistance
