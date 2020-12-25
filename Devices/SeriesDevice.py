#Sub class of Device, defines a new Series device which can contain other devices

from Device import *
from ParallelDevice import *
from Resistor import *
class SeriesDevice(Device):
    def __init__(self, leftDevice, rightDevice):
        if (leftDevice == None and rightDevice == None):
            super().__init__(None, None)
        elif (leftDevice == None):
            super().__init__(None, rightDevice.getTail())
        elif (rightDevice == None):
            super().__init__(leftDevice.getHead(), None)
        else:
            super().__init__(leftDevice.getHead(), rightDevice.getTail())
        self.allDevices = []
        if (leftDevice != None):
            self.allDevices.append(leftDevice)
        if (rightDevice != None):
            self.allDevices.appen(rightDevice)
    def getAllDevices(self):
        return self.allDevices
    
    def addHead(self, device):
        self.setHead(device.getHead())
        self.allDevices.insert(0, device)

    def addTail(self, device):
        self.setTail(device.getTail())
        self.allDevices.append(device)
    
    def strForm(self):
        return self.parallelOrSeriesStrForm()
    
    def __repr__(self):
        return self.strForm()

    #recursive approach to printing all devices
    def parallelOrSeriesStrForm(self, indent = ""):
        retStr = "Series Device - {"
        parallelDevices = []
        for eachDevice in self.allDevices:
            if (isinstance(eachDevice, ParallelDevice)):
                parallelDevices.append(eachDevice)
                retStr += "(Parallel " + str(len(parallelDevices)) + "),       "
            else:
                retStr += eachDevice.strForm() + ",       "
        
        if (len(parallelDevices) == 0):
            return retStr[:-8] + "}"
        retStr = retStr[:-8] + "}" + "\n"

        i = 1
        for eachParallel in parallelDevices:
            retStr += str(i) + ": " + eachParallel.strForm() + ",       "
            i += 1

        return retStr[:-9]
    
    def setCurrentForAllDevices(self, current):
        for eachDev in self.allDevices:
            eachDev.currentAcross = current
            eachDev.voltAcross = eachDev.currentAcross * eachDev.resistanceAcross
            if (isinstance(eachDev, ParallelDevice)):
                for eachBranch in eachDev.allDevices:
                    if (isinstance(eachBranch, Resistor)):
                        eachBranch.voltAcross = round(eachDev.voltAcross, 4)
                        eachBranch.currentAcross = round((eachDev.voltAcross / eachBranch.resistance) * 1000, 4)
                    else:
                        eachBranch.voltAcross = eachDev.voltAcross
                        eachBranch.currentAcross = eachDev.voltAcross / eachBranch.resistanceAcross
                        eachBranch.setCurrentForAllDevices(eachBranch.currentAcross)
            else:
                eachDev.currentAcross = round(eachDev.currentAcross * 1000, 4)
                eachDev.voltAcross = round(eachDev.voltAcross, 4)

    #solves the circuit
    def solveCircuit(self):
        batteryVoltage = self.allDevices[0].voltage
        battery = self.allDevices[0]
        self.allDevices = self.allDevices[1:]
        totRes = self.resistanceBreakdown()
        totCurrent = batteryVoltage / totRes
        battery.currentAcross = round(totCurrent * 1000, 4)
        battery.voltAcross = batteryVoltage
        
        self.setCurrentForAllDevices(totCurrent)

    #recursive approach to resistance breakdown
    def resistanceBreakdown(self):
        totalResistance = 0
        for eachDevice in self.allDevices: #iterates through all devices in self
            if (isinstance(eachDevice, Resistor)):
                totalResistance += eachDevice.resistance
            elif (isinstance(eachDevice, ParallelDevice)): #recursive case when device is a ParallelDevice
                eachBranchRes = []
                for eachBranch in eachDevice.allDevices:
                    if (isinstance(eachBranch, Resistor)):
                        eachBranchRes.append(eachBranch.resistance)
                    else:
                        eachBranch.resistanceAcross = eachBranch.resistanceBreakdown()
                        eachBranchRes.append(eachBranch.resistanceAcross)
                totRes = 0
                for i in eachBranchRes:
                    if (i == 0):
                        continue
                    totRes += 1 / i
                totalResistance += 1 / totRes
                eachDevice.resistanceAcross = 1 / totRes
        return totalResistance

    
