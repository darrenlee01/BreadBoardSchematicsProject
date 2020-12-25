

#Super class for breadboard devices
#kind of the front end of the breadboard mode

from Node import *
import math # Following code from math

class DeviceBread():
    def __init__(self, url, scale, n1x, n1y, n2x, n2y, declareNodes = True):
        if (declareNodes):
            self.n1 = Node([self], n1x, n1y)
            self.n2 = Node([self], n2x, n2y)
        self.url = url
        self.scale = scale
        self.angle = 0
        self.calculateAngle()
        
        self.cx = 0
        self.cy = 0
        self.calculateCenter()

        self.deviceForm = None
        self.voltAcross = 0
        self.currAcross = 0
    
    def setDeviceForm(self, device):
        self.deviceForm = device
        
    def setVoltAndCurr(self):
        self.voltAcross = self.deviceForm.voltAcross
        self.currAcross = self.deviceForm.currentAcross
    
    def setToNewNode(self, nodeNum):
        if (nodeNum == 1):
            self.setN1(Node([self], 0, 0))
        else:
            self.setN2(Node([self], 0, 0))
    def setN1(self, newNode):
        self.n1 = newNode
    def setN2(self, newNode):
        self.n2 = newNode
    def getOpposNode(self, excludingNode):
        if (excludingNode == self.getNode1()):
            return self.getNode2()
        else:
            return self.getNode1()

    def getNode1(self):
        return self.n1

    def getNode2(self):
        return self.n2

    def setNode1Pos(self, x, y):
        self.getNode1().x = x
        self.getNode1().y = y
        self.calculateCenter()

    def setNode2Pos(self, x, y):
        self.getNode2().x = x
        self.getNode2().y = y
        self.calculateCenter()
    
    def refactorDevice(self):
        self.calculateCenter()
        self.calculateAngle()

    def calculateCenter(self):
        self.cx = (self.getNode1().x + self.getNode2().x) / 2
        self.cy = (self.getNode1().y + self.getNode2().y) / 2

    #calculates the angle needed to turn the breadboard image
    def calculateAngle(self):
        (node1x, node1y, node2x, node2y) = (self.getNode1().x, self.getNode1().y
                            , self.getNode2().x, self.getNode2().y)
        horizSide = node2x - node1x
        vertSide = node1y - node2y
        if (horizSide == 0):
            if (vertSide > 0):
                self.angle = 90
            else:
                self.angle = 270

        else:

            self.angle = (math.atan(abs( vertSide / horizSide)) * 180) / math.pi
            if (horizSide >= 0):
                if (vertSide < 0):
                    self.angle = 360 - self.angle
            else:
                self.angle = (math.atan(abs(vertSide / horizSide)) * 180) / math.pi
                if (vertSide >= 0):
                    self.angle = 180 - self.angle
                else:
                    self.angle = (math.atan(abs(horizSide / vertSide)) * 180) / math.pi
                    self.angle = (270 - self.angle)

    def notCompletelyConnected(self):
        return len(self.getNode1().connectedDevices) == 0 or self.getNode2().numConnected() == 0

    def nodeDist(self):
        return ((self.getNode1().x - self.getNode2().x) ** 2 + 
                    (self.getNode1().y  - self.getNode2().y) ** 2) ** 0.5
    
    def __repr__(self):
        print("abstract method for repr!")
        assert(False)

    def toDevice(self, leftDevice, rightDevice):
        print("Override toDevice function")
        assert(False)

    def getConnectedToNode1(self):
        ret = []
        for each in self.getNode1().connectedDevices:
            if (each != self):
                ret.append(each)
        return ret
    
    def getConnectedToNode2(self):
        ret = []
        for each in self.getNode2().connectedDevices:
            if (each != self):
                ret.append(each)
        return ret

    def connectedInParallel(self):
        return (self.getNode1() == obj.getNode1()
                                    and self.getNode2() == obj.getNode2())
