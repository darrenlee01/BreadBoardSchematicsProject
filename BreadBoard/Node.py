#class for the 2 nodes on each of the devices

class Node():
    nodeWidth = 4

    def __init__(self, connectedDevices, x, y):
        #connected devices inclues itself
        self.connectedDevices = connectedDevices
        self.x = x
        self.y = y
        self.occupyingHole = None
    
    def addDevice(self, device):
        self.connectedDevices.append(device)
    
    def removeDevice(self, device):
        self.connectedDevices.remove(device)
    
    def getConnectedDevicesExcluding(self, deviceList):

        ret = []
        for eachSch in self.connectedDevices:
            
            if (eachSch not in deviceList):
                ret.append(eachSch)
                
        return ret

    def numConnected(self):
        return len(self.connectedDevices) - 1

    def getConnectedDevices(self):
        return self.connectedDevices
    
    def setConnectedDevices(self, lst):
        self.connectedDevices = lst
    
    def getConnectedToNode(self, device):
        ret = []
        for each in self.connectedDevices:
            if (each != device):
                ret.append(each)
        return ret
    
    #combines self and Node toCombine without overlap
    #sets toCombine to point to self
    def combineNodes(self, toCombine):
        for eachDevice in toCombine.getConnectedDevices():
            #if there are 2 devices in each list pointing to the same thing
            #do not add
            if (eachDevice not in self.getConnectedDevices()):
                self.getConnectedDevices().append(eachDevice)
        toCombine.setConnectedDevices(self.getConnectedDevices())
    
    def combineNodesTest(self, toCombine):
        for eachDevice in toCombine.getConnectedDevices():
            #if there are 2 devices in each list pointing to the same thing
            #do not add
            if (eachDevice not in self.getConnectedDevices()):
                self.getConnectedDevices().append(eachDevice)
     
    def __eq__(self, obj):
        return isinstance(obj, Node) and self.connectedDevices == obj.connectedDevices

    def __repr__(self):
        if (self.occupyingHole != None):
            return str(self.occupyingHole)
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    