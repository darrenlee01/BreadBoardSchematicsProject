#Sub class of DeviceSchematic, defines a Schematic Battery

from DeviceSchematic import *

import sys # Following code from sys
sys.path.append("C:/Users/Darren/Documents/Python/15-112/Term Project/Devices")
sys.path.append("Devices")
#learned to use sys from Stack Overflow
#https://stackoverflow.com/questions/4383571/importing-files-from-different-folder

from Battery import *
class BatterySchematic(DeviceSchematic):
    url = "Battery.png"      #self-made vector image
    scale = 0.2
    cropDim = None
    height = 56

    def __init__(self, n1x, n1y, n2x, n2y, voltage):
        self.posNode = Node([self], n1x, n1y)
        self.negNode = Node([self], n2x, n2y)
        super().__init__(BatterySchematic.url, BatterySchematic.scale,
                                    n1x, n1y, n2x, n2y, False)

        self.voltage = voltage
    
    def setN1(self, newNode):
        self.posNode = newNode

    def setN2(self, newNode):
        self.negNode = newNode

    def toDevice(self, tail):
        deviceForm = Battery(tail, self.voltage)
        return deviceForm
        
    
    def getNode1(self):
        return self.posNode

    def getNode2(self):
        return self.negNode
    
    def __repr__(self):
        return "Battery - (" + str(self.cx) + ", " + str(self.cy) + ")"
