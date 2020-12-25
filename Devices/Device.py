#Super class which defines a new device
#kind of the backend work of this program

class Device():
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail
        self.voltAcross = None
        self.resistanceAcross = None
        self.currentAcross = None
        

    def getHead(self):
        return self.head

    def getTail(self):
        return self.tail

    def setHead(self, connection):
        self.head = connection
    
    def setTail(self, connection):
        self.tail = connection
    
    def isSerialConnected(self, device):
        if (self.getHead() == device and self.getTail() == device):
            return False
        return (self.getHead() == device or 
                    self.getTail() == device)
    
    def isParallelConnected(self, device):
        return (self.getHead() == device.getHead() and
                    self.getTail() == device.getTail())

    #abstract method
    def strForm(self):
        print("Did not override strForm in Device class")
        assert(False)

