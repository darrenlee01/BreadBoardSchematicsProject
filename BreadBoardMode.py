#Breadboard mode: handles the animations in this mode

import sys # Following code from sys
#sys.path.append("C:/Users/Darren/Documents/Python/15-112/Term Project/Devices")
#sys.path.append("C:/Users/Darren/Documents/Python/15-112/Term Project/BreadBoard")
sys.path.append("Devices")
sys.path.append("BreadBoard")
#learned to use sys from Stack Overflow
#https://stackoverflow.com/questions/4383571/importing-files-from-different-folder

from WireBread import *
from DeviceBread import *
from ResistorBread import *
from Hole import *

from cmu_112_graphics import *
# Following framework from cmu_112_graphics

from PIL import Image
# Following code from Image
import PIL
# Following code from PIL

from Device import *
from SeriesDevice import *
from ParallelDevice import *
from Resistor import *
from Battery import *

class BreadBoardMode(Mode):
    def appStarted(app):
        
        midW = app.width / 2
        midH = app.height / 2
        app.allBreads = [] #list of bread board devices
        app.posRailConnected = [] #list of bread board devices connected to positive rail
        app.negRailConnected = [] #list of bread board devices connected to negative rail

        app.selectedNode = None #the selected node by the user
        app.connectedHole = None #the hole that got connected by the selected node

        app.priorConnectedHole = None
        app.showCircAnalysis = False #boolean for checking if circuit analysis should be shown

        breadBoardUrl = "Bread Board.png"
        # Following picture from https://pcbways.blogspot.com/1970/01/breadboard-layout-diagram.html
        # added numbering with vector file editor

        app.breadBoardImage = app.loadImage(breadBoardUrl)
        app.breadBoardImage = app.scaleImage(app.breadBoardImage, 0.9)
        app.allHoles = [] #all holes in the board
        app.mainHoles = [] #all the main holes on the board

        app.posHoles = [] #all positive holes on the board
        app.negHoles = [] #all positive holes on the board

        #initializes main holes, neg holes, pos holes
        app.mainBreadBoardCoords()
        app.negCoords()
        app.posCoords()

        app.isReady = False

    def defineBattery(app):
        inputVolt = app.getUserInput('Input DC Voltage in Volts')
        if (inputVolt == None or not inputVolt.isdigit()):
            inputVolt = "5"
        app.batteryVolt = int(inputVolt)

    @staticmethod
    def dist(x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1  - y2) ** 2) ** 0.5
    
    def negCoords(app):
        x = 233
        y = 233
        dx = 17.5
        interval = 37
        
        for eachInt in range(10):
            for eachDot in range(5):
                h = Hole(x, y, isMainBoard = -1)
                app.allHoles.append(h)
                app.negHoles.append(h)
                x += dx
            x += interval - dx

        x = 233
        y = 553
        for eachInt in range(10):
            for eachDot in range(5):
                h = Hole(x, y, isMainBoard = -1)
                app.allHoles.append(h)
                app.negHoles.append(h)
                x += dx
            x += interval - dx
    def posCoords(app):
        x = 233
        y = 250
        dx = 17.5
        interval = 37

        for eachInt in range(10):
            for eachDot in range(5):
                h = Hole(x, y, isMainBoard = 1)
                app.allHoles.append(h)
                app.posHoles.append(h)
                x += dx
            x += interval - dx

        x = 233
        y = 571
        for eachInt in range(10):
            for eachDot in range(5):
                h = Hole(x, y, isMainBoard = 1)
                app.allHoles.append(h)
                app.posHoles.append(h)
                x += dx
            x += interval - dx
    def mainBreadBoardCoords(app):
        firstX = 198
        firstY = 303
        x = firstX
        y = firstY
        dX = 17.8
        dY = 18
        startC = 63

        for c in range(63):
            fullCol = []
            for r in range(5):
                newHole = Hole(x, y, c, r)
                fullCol.append(newHole)
                app.allHoles.append(newHole)
                y += dY
            app.mainHoles.append(fullCol)
            y = firstY
            x += dX
        firstY = 428
        y = firstY
        x = firstX

        for c in range(startC, startC + 63):
            fullCol = []
            for r in range(5):
                newHole = Hole(x, y, c, r)
                fullCol.append(newHole)
                app.allHoles.append(newHole)
                y += dY
            app.mainHoles.append(fullCol)
            y = firstY
            x += dX


    def keyPressed(app, event):
        if (not app.isReady):
            return
        if (event.key == "r"): #new resistor
            inputRes = app.getUserInput('Input resistance in kilo Ohms')
            if (inputRes == None or not inputRes.isdigit()):
                inputRes = "1"
            r = ResistorBread(100, 300, 100, 500, int(inputRes) * 1000)
            i = app.breadToImage(r)
            app.allBreads.append([r, i])
            app.showCircAnalysis = False
        elif (event.key == "s"): #show connections
            print()
            for i in app.posHoles:
                if (i.occupyingDevice != None):
                    print("Device", i.occupyingDevice)
                    print("occupying node", i.occupyingNode)
            
            print()
            print()
            for i in range(len(app.allBreads)):
                print("current device", app.allBreads[i][0])
                print("1", app.allBreads[i][0].getNode1())
                print("2", app.allBreads[i][0].getNode2())
                print("Node 1", app.allBreads[i][0].getNode1().getConnectedDevices())
                print("Node 2", app.allBreads[i][0].getNode2().getConnectedDevices())
                print()
            print()
            print()
        elif (event.key == "Delete"): #delete last added device
            if (len(app.allBreads) == 0):
                app.app.showMessage("No more devices to delete!")
                return
            deviceToDelete = -1 #need to change, only used for proof of concept
            currDevice = app.allBreads[deviceToDelete][0]
            node1 = app.allBreads[deviceToDelete][0].getNode1()
            node2 = app.allBreads[deviceToDelete][0].getNode2()
            node1.removeDevice(currDevice)
            node2.removeDevice(currDevice)
            if (node1.occupyingHole != None):
                node1.occupyingHole.removeOccupied()
            if (node2.occupyingHole != None):
                node2.occupyingHole.removeOccupied()

            app.allBreads.pop(deviceToDelete)
            app.showCircAnalysis = False
        elif (event.key == "w"): #add wire
            w = WireBread(120, 300, 120, 500)
            app.allBreads.append([w, None])
            app.showCircAnalysis = False
        elif (event.key == "h"): #show all connected holes
            print()
            for i in app.allHoles:
                if (i.occupyingDevice != None):
                    print(i)
            print()
        elif (event.key == "c"): #shows circ analysis
            app.showCircAnalysis = True
            circ = app.breadsToDevices()
            if (type(circ) == str):
                app.showCircAnalysis = False
                app.app.showMessage(circ)
            else:
                print()
                print(circ)
                print()
                circ.solveCircuit()
        elif (event.key == "R"): #restart mode
            app.appStarted()
        
        elif (event.key == "S"): #switch modes if circuit is complete
            app.app.convertCircuit = app.breadsToDevices(converting = True)
            
            if (type(app.app.convertCircuit) == str):
                app.app.showMessage(app.app.convertCircuit)
                app.showCircAnalysis = False
                return
            if (type(app.app.convertCircuit.allDevices[-1]) == ParallelDevice):
                app.app.convertCircuit.allDevices.append(Resistor(None, None, 0))
            if (type(app.app.convertCircuit.allDevices[1]) == ParallelDevice):
                app.app.convertCircuit.allDevices.insert(1, Resistor(None, None, 0))
            app.app.schematicsMode.showCircAnalysis = False
            app.app.setActiveMode(app.app.schematicsMode)
    

    def breadToImage(app, bread): #converts bread to image
        image = app.loadImage(bread.url)
        image = app.scaleImage(image, bread.scale)
        if (bread.cropDim != None):
            image = image.crop(bread.cropDim)
        image = image.rotate(bread.angle, PIL.Image.NEAREST, expand = 1)
        return image

    #function for converting breadboard connections to device format
    #goes through each node to do conversion
    def breadsToDevices(app, converting = False):
        currNode = app.firstConnectedNode(app.posHoles)
        endNode = app.firstConnectedNode(app.negHoles)
        if (currNode == None or endNode == None):
            return "Positive or Negative Rail is not connected!"
        if (len(app.allBreads) == 1):
            return "Add more than 1 device!"
        connectionsInNode = currNode.getConnectedDevices()
        batteryDevice = Battery(None, app.batteryVolt)

        circuit = SeriesDevice(batteryDevice, None)
        priorDevice = batteryDevice

        while (currNode != endNode):
            
            #series case
            if (len(connectionsInNode) == 1):
                currBread = connectionsInNode[0]

                currDevice = currBread.toDevice(priorDevice, None)
                currBread.setDeviceForm(currDevice)
                circuit.addTail(currDevice)
                priorDevice.setTail(currDevice)
                currDevice.setHead(priorDevice)
                priorDevice = currDevice

                if (currBread.getNode1() == currNode):
                    currNode = currBread.getNode2()
                else:
                    currNode = currBread.getNode1()
                connectionsInNode = currNode.getConnectedToNode(currBread)
            else: #parallel case
                devicesInNode = []
                parallelEndingNode = None
                toExclude = []
                for i in range(len(connectionsInNode)): #goes through each branch of the parallel case

                    startingBread = connectionsInNode[i]
                    startingDev = startingBread.toDevice(None, None)
                    startingBread.setDeviceForm(startingDev)
                    nextNode = startingBread.getOpposNode(currNode)
                    nextNodeConnections = nextNode.getConnectedToNode(startingBread)
                    currSeriesBranch = SeriesDevice(startingDev, None)
                    totRes = startingDev.resistance

                    lastInBranch = [startingBread]
                    
                    while (True): #while there is another device in the parallel branch
                        print(currSeriesBranch)
                        print(nextNode)
                        
                        if (nextNode == endNode): #done with this parallel branch
                            parallelEndingNode = endNode
                            break
                        if (len(nextNodeConnections) == 1): #there is a device in series in this particular branch
                            addSeries = nextNodeConnections[0].toDevice(None, None)
                            totRes += addSeries.resistance

                            nextNodeConnections[0].setDeviceForm(addSeries)
                            currSeriesBranch.addTail(addSeries)
                            lastInBranch = [nextNodeConnections[0]]
                            
                            nextNode = nextNodeConnections[0].getOpposNode(nextNode)
                            nextNodeConnections = nextNode.getConnectedToNode(nextNodeConnections[0])

                        else: #parallel node, must check if this is the ending node for this parallel case
                            print("next node conns:", nextNodeConnections)
                            nestedParallelDev = []
                            isSimpleParallel = True
                            if (len(nextNodeConnections) <= 1):
                                return "Disconnected node!"
                            for j in range(len(nextNodeConnections) - 1):
                                firstNode = nextNodeConnections[j].getOpposNode(nextNode)
                                secNode = nextNodeConnections[j + 1].getOpposNode(nextNode)
                                if (firstNode != secNode):
                                    isSimpleParallel = False
                                    
                                    toExclude.extend(lastInBranch)
                                    if (parallelEndingNode == None):
                                        parallelEndingNode = nextNode
                                    else:
                                        if (parallelEndingNode != nextNode):
                                            return "Cannot handle this circuit!"
                                    break

                            if (not isSimpleParallel):
                                print("done")
                                break
                            else:
                                return "Cannot handle this circuit!"
                    if (totRes == 0):
                        return "Short Circuit!"
                        
                    if (len(currSeriesBranch.getAllDevices()) == 1): #if this branch is just 1 device
                        toExclude.extend([])
                        if (converting == True):
                            currSeriesBranch.allDevices.append(Resistor(None, None, 0))
                            devicesInNode.append(currSeriesBranch)
                        else:
                            devicesInNode.append(currSeriesBranch.getAllDevices()[0])
                    else:
                        devicesInNode.append(currSeriesBranch)
                
                currParallel = ParallelDevice(devicesInNode)
                currParallel.setHead(priorDevice)
                priorDevice.setTail(currParallel)
                circuit.addTail(currParallel)
                priorDevice = currParallel
                if (parallelEndingNode == None):
                    if (len(connectionsInNode) == 0):
                        return "Disconnected node!"
                    currNode = connectionsInNode[0].getOpposNode(currNode)
                    connectionsInNode = currNode.getConnectedDevicesExcluding(connectionsInNode)
                else:
                    
                    currNode = parallelEndingNode
                    connectionsInNode = currNode.getConnectedDevicesExcluding(toExclude)
            
        return circuit
    
    def mousePressed(app, event):
        if (not app.isReady):
            if (app.app.askVoltage):
                
                app.defineBattery()
            else:
                app.app.askVoltage = True
            app.isReady = True
            return

        index = 0
        for index in range(len(app.allBreads)): #must check all nodes to see which is the selectedNode
            eachDevice = app.allBreads[index][0]
            currentNode1 = eachDevice.getNode1()
            currentNode2 = eachDevice.getNode2()
            if (app.dist(event.x, event.y, currentNode1.x, currentNode1.y) <= Node.nodeWidth):
                app.selectedNode = (index, 1)
                
                if (currentNode1.occupyingHole != None):
                    app.priorConnectedHole = currentNode1.occupyingHole

                return
            elif (app.dist(event.x, event.y, currentNode2.x, currentNode2.y) <= Node.nodeWidth):
                app.selectedNode = (index, 2)
                if (currentNode2.occupyingHole != None):
                    app.priorConnectedHole = currentNode2.occupyingHole 
                return

    def mouseDragged(app, event):
        if (app.selectedNode != None): #if there is a selectedNode
            app.showCircAnalysis = False

            (i, num) = app.selectedNode
            movingDevice = app.allBreads[i][0]
            
            movingNodeX = event.x
            movingNodeY = event.y

            oppositeNodeX = 0
            oppositeNodeY = 0
            if (num == 1):
                currNode = movingDevice.getNode1()
                oppositeNodeX = movingDevice.getNode2().x
                oppositeNodeY = movingDevice.getNode2().y
            else:
                currNode = movingDevice.getNode2()
                oppositeNodeX = movingDevice.getNode1().x
                oppositeNodeY = movingDevice.getNode1().y
            
            #if there is a prior connected hole
            if (app.priorConnectedHole != None):
                app.priorConnectedHole.occupyingNode = None
                app.priorConnectedHole.occupyingDevice = None

                currNode.removeDevice(movingDevice)
                movingDevice.setToNewNode(num)

                app.priorConnectedHole = None
                
            #stop moving if the 2 nodes are less than the device height
            if (app.dist(event.x, event.y, oppositeNodeX, oppositeNodeY) <= movingDevice.height):
                if (not isinstance(movingDevice, WireBread)):
                    app.allBreads[i][1] = app.breadToImage(movingDevice)
                    movingDevice.calculateCenter()
                    movingDevice.calculateAngle()
                return
            
            for eachHole in app.allHoles:
                (holeX, holeY) = (eachHole.x, eachHole.y)
                if (eachHole.occupyingNode != None or eachHole.occupyingDevice != None):
                    continue
                if (app.dist(event.x, event.y, holeX, holeY) <= Node.nodeWidth * 2):
                    app.connectedHole = eachHole
                    movingNodeX = holeX
                    movingNodeY = holeY
                    break
       
            if (num == 1):
                movingDevice.setNode1Pos(movingNodeX, movingNodeY)
            elif (num == 2):
                movingDevice.setNode2Pos(movingNodeX, movingNodeY)

            if (not isinstance(movingDevice, WireBread)):
                app.allBreads[i][1] = app.breadToImage(movingDevice)
                movingDevice.refactorDevice()
    
    def mouseReleased(app, event):
        app.priorConnectedHole = None
        if (app.selectedNode == None):
            return
        
        (i, num) = app.selectedNode
        movingDevice = app.allBreads[i][0]
        selNode = 0

        if (num == 1):
            selNode = movingDevice.getNode1()
        else:
            selNode = movingDevice.getNode2()
        
        #making sure that the selected node and the connected hole are in place
        if (selNode != None and app.connectedHole.x == selNode.x and 
                    app.connectedHole.y == selNode.y):
            
            if (app.connectedHole.isMainBoard == 0): #is main board
                checkRow = app.mainHoles[app.connectedHole.row]
                firstConnected = app.firstConnectedNode(checkRow, excCol = app.connectedHole.col)
                if (firstConnected != None):
                    firstConnected.combineNodes(selNode)
            elif (app.connectedHole.isMainBoard > 0): #is pos rail
                checkRow = app.posHoles
                firstConnected = app.firstConnectedNode(checkRow, excHole = app.connectedHole)
                if (firstConnected != None):
                    firstConnected.combineNodes(selNode)
            else: #is neg rail
                checkRow = app.negHoles
                firstConnected = app.firstConnectedNode(checkRow, excHole = app.connectedHole)
                if (firstConnected != None):
                    firstConnected.combineNodes(selNode)

            app.connectedHole.occupyingNode = selNode
            app.connectedHole.occupyingDevice = movingDevice
            selNode.occupyingHole = app.connectedHole

        app.selectedNode = None

    #checks the particular row and returns the first connected device
    def firstConnectedNode(app, row, excCol = None, excHole = None):
        for col in range(len(row)):
            if (col == excCol):
                continue
            eachHole = row[col]
            if (excHole != None and excHole == eachHole):
                continue
            if (eachHole.occupyingNode != None and eachHole.occupyingDevice != None):
                return eachHole.occupyingNode
        return None

    def drawBreadBoard(app, canvas):
        canvas.create_text(app.width / 2, 70, text = "Breadboard", font = "Arial 60 bold")

        canvas.create_image(app.width / 2, app.height / 2, image=ImageTk.PhotoImage(app.breadBoardImage))
    
    #draws the bread board device
    def drawDevice(app, canvas, bread, image):
        nodeR = 4
        node1 = bread.getNode1()
        node2 = bread.getNode2()
        (n1X, n1Y, n2X, n2Y) = (node1.x, node1.y, node2.x, node2.y)
        canvas.create_line(n1X, n1Y, n2X, n2Y, width = 4, fill = "dark grey")
        canvas.create_oval(n1X - nodeR, n1Y - nodeR, n1X + nodeR, n1Y + nodeR, 
                                                            fill = "white", width = 3)
        canvas.create_oval(n2X - nodeR, n2Y - nodeR, n2X + nodeR, n2Y + nodeR, 
                                                            fill = "white", width = 3)
        if (not isinstance(bread, WireBread)):
            canvas.create_image(bread.cx, bread.cy, image=ImageTk.PhotoImage(image))
     
    def redrawAll(app, canvas):
        
        if (not app.isReady):
            canvas.create_text(app.width / 2, app.height / 2, text = "Click to Start!", font = "Arial 60 bold")
            return

        app.drawBreadBoard(canvas)
        canvas.create_text(1450, 400, text = str(app.batteryVolt) + " V", 
                                    font = "Arial 30 bold")
        usedRows = set()

        #draws each of the devices
        for (breadDevice, image) in app.allBreads:
            hole1 = breadDevice.n1.occupyingHole
            hole2 = breadDevice.n2.occupyingHole
            if (hole1 != None and hole1.isMainBoard == 0):
                usedRows.add(hole1.row)
            if (hole2 != None and hole2.isMainBoard == 0):
                usedRows.add(hole2.row)

            app.drawDevice(canvas, breadDevice, image)
            if (type(breadDevice) == ResistorBread):
                canvas.create_text(breadDevice.cx, breadDevice.cy, 
                    text = str(breadDevice.getResistance()) + " Ohms",
                    font = "Arial 12 bold", fill = "red")
            if (breadDevice.deviceForm != None and app.showCircAnalysis):

                canvas.create_text(breadDevice.cx, breadDevice.cy + 15, 
                    text = (str(breadDevice.deviceForm.voltAcross) + 
                        " V, " + str(breadDevice.deviceForm.currentAcross) + " mA"),
                    font = "Arial 12 bold", fill = "red")
        
        #draws a line for each row used on the breadboard
        for eachRow in usedRows:
            x = app.mainHoles[eachRow][0].x
            y1 = app.mainHoles[eachRow][0].y
            y2 = app.mainHoles[eachRow][-1].y
            canvas.create_line(x, y1, x, y2, fill = "lime", width = 2)