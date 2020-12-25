#Sub class of Device, defines a Parallel Device which can contain other devices

from Device import *
from SeriesDevice import *
class ParallelDevice(Device):
    def __init__(self, devicesInParallel):
        if (not isinstance(devicesInParallel, list)):
            print("Incompatible types in ParallelDevice constructor")
            assert(False)
        #all devices in list should have the same connections
        super().__init__(None, None)
        self.allDevices = devicesInParallel

    def numInParallel(self):
        return len(self.allDevices)

    def addDevice(self, device):
        self.allDevices.append(device)
    
    def strForm(self):
        return self.parallelOrSeriesStrForm()
    
    def __repr__(self):
        return self.strForm()
    
    #recursive approach to printing all devices
    def parallelOrSeriesStrForm(self, indent = ""):
        retStr = " Parallel Device - ["
        parallelDevices = []
        for eachDevice in self.allDevices:
            if (isinstance(eachDevice, ParallelDevice)):
                parallelDevices.append(eachDevice)
                retStr += "(Parallel " + str(len(parallelDevices)) + "),       "
            else:
                retStr += eachDevice.strForm() + ",       "
        
        if (len(parallelDevices) == 0):
            return retStr[:-8] + "]"
        retStr = retStr[:-8] + "]" + "\n"

        i = 1
        for eachParallel in parallelDevices:
            retStr += str(i) + ": " + eachParallel.strForm() + ",       "
            i += 1

        return retStr[:-9]
