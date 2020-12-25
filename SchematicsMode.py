#Schematics mode: handles the animations in this mode

import sys # Following code from sys
#sys.path.append("C:/Users/Darren/Documents/Python/15-112/Term Project/Devices")
#sys.path.append("C:/Users/Darren/Documents/Python/15-112/Term Project/Schematics")
sys.path.append("Devices")
sys.path.append("Schematics")
#learned to use sys from Stack Overflow
#https://stackoverflow.com/questions/4383571/importing-files-from-different-folder

from WireSchematic import *
from DeviceSchematic import *
from BatterySchematic import *
from ResistorSchematic import *

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
from Wire import *

class SchematicsMode(Mode):
    def appStarted(app):

        app.allSchematics = [] #stores all schematic devices

        app.selectedNode = None #the selected node by the user
        app.connectedNode = None #the hole that got connected by the selected node

        app.isConnectedNode = False

        app.showCircAnalysis = False #boolean for checking if circuit analysis should be shown
        app.isReady = False

    #makes a Schematic battery
    def defineBattery(app):
        midW = app.width / 2
        midH = app.height / 2
        
        if (app.app.askVoltage):

            inputVolt = app.getUserInput('Input DC Voltage in Volts')
            if (inputVolt == None or not inputVolt.isdigit() or inputVolt == "0"):
                inputVolt = "5"
        else:
            inputVolt = app.batteryVolt
            print(inputVolt)
            app.app.askVoltage = True
        app.b = BatterySchematic(100, midH / 2, 100, midH * 1.5, int(inputVolt))
        app.bImage = app.schematicToImage(app.b)
        app.allSchematics.append([app.b, app.bImage])
    
    def insideCanvas(app, x, y):
        if (x <= 0 or x >= app.width or y <= 0 or y >= app.height):
            return False
        return True

    #converts devices to schematic 
    #used for converting breadboard to schematic
    def deviceToSchematics(app):
        app.allSchematics = []

        battDev = app.app.convertCircuit.allDevices[0]

        app.b = BatterySchematic(100, app.height / 4, 100, app.height / 2 * 1.5, battDev.voltage)
        app.bImage = app.schematicToImage(app.b)
        app.allSchematics.append([app.b, app.bImage])
        app.app.convertCircuit.allDevices.pop(0)

        currNode = app.b.getNode1()
        endNode = app.b.getNode2()

        dx = 200
        dy = 0

        for i in range(len(app.app.convertCircuit.allDevices)):
            eachDev = app.app.convertCircuit.allDevices[i]

            #series case
            if (isinstance(eachDev, Resistor)):
                x0 = currNode.x
                y0 = currNode.y
                x1 = currNode.x + dx
                y1 = currNode.y + dy
                mag = 0
                isX = True

                #finds a possible node inside the canvas
                while (True):
                    if (x1 >= app.width):
                        dx = -10 * mag
                        dy = 200
                    elif (x1 <= 0):
                        dx = 10 * mag
                        dy = -200
                    elif (y1 >= app.height):
                        dx = -200
                        dy = -10 * mag
                        isX = False
                    elif (y1 <= 0):
                        dx = 200
                        dy = 10 * mag
                        isX = False
                    else:
                        print(dx, dy)
                        if (not isX):
                            dx = 0
                        else:
                            dy = 0
                        break
                    x1 = currNode.x + dx
                    y1 = currNode.x + dy
                    mag += 1
                dev = None
                if (eachDev.resistance == 0):
                    dev = WireSchematic(x0, y0, x1, y1)
                else:
                    dev = ResistorSchematic(x0, y0, x1, y1, eachDev.resistance)
                
                #combines with prior device's node
                currNode.combineNodes(dev.getNode1())
                currNode = dev.getNode2()

                if (i == len(app.app.convertCircuit.allDevices) - 1): #if this is the last device to convert
                    currNode.combineNodes(endNode)
                    currNode.x = endNode.x
                    currNode.y = endNode.y
                dev.refactorDevice()
                if (dev.resistance > 0): #if this is a resistor
                    
                    rImage = app.schematicToImage(dev)
                    app.allSchematics.append([dev, rImage])
                else: #if this is a wire
                    app.allSchematics.append([dev, None])

            #parallel case
            elif (type(eachDev) == ParallelDevice):
                paralEndNode = None
                if (i == len(app.app.convertCircuit.allDevices) - 1): #if this is the last device in the circuit
                    paralEndNode = endNode
                startAng = 0
                dAng = 0  #goes counter clockwise
                radius = 200
                
                #places each branch in about a 90 degree range
                #this range is pointed towards the center of the canvas
                if (currNode.x > app.width / 2):
                    if (currNode.y > app.height / 2):
                        startAng = 0.6 * math.pi
                    else:
                        startAng = 1.1 * math.pi
                else:
                    if (currNode.y > app.height / 2):
                        startAng = 0.1 * math.pi
                    else:
                        startAng = 1.6 * math.pi
                dAng = (0.4 * math.pi) / len(eachDev.allDevices)

                #iterates through each branch of the parallel device
                for j in range(len(eachDev.allDevices)):
                    parallStartNode = currNode
                    eachDevInBranch = eachDev.allDevices[j]
                    if (type(eachDevInBranch) == SeriesDevice): #if the branch is a series device
                        nextNode = parallStartNode
                        for k in range(len(eachDevInBranch.allDevices)): #iterate through the series device
                            currSerDev = eachDevInBranch.allDevices[k]

                            #if this is the last device of the series branch and the end node has been found
                            if (k == len(eachDevInBranch.allDevices) - 1 and paralEndNode != None):
                                x0 = nextNode.x
                                y0 = nextNode.y
                                x1 = paralEndNode.x
                                y1 = paralEndNode.y
                                dev = None
                                if (currSerDev.resistance == 0):
                                    dev = WireSchematic(x0, y0, x1, y1)
                                    dev.refactorDevice()
                                    app.allSchematics.append([dev, None])
                                else:
                                    dev = ResistorSchematic(x0, y0, x1, y1, currSerDev.resistance)
                                    dev.refactorDevice()
                                    rImage = app.schematicToImage(dev)
                                    app.allSchematics.append([dev, rImage])
                                nextNode.combineNodes(dev.getNode1())
                                paralEndNode.combineNodes(dev.getNode2())
                                
                            else:
                                x0 = nextNode.x
                                y0 = nextNode.y
                                x1 = nextNode.x + radius * math.cos(startAng)
                                y1 = nextNode.y - radius * math.sin(startAng)
                                newAng = startAng
                                while (not app.insideCanvas(x1, y1)): #finds a possible angle if not inside canvas
                                    newAng += math.pi / 10
                                    x1 = nextNode.x + radius * math.cos(newAng)
                                    y1 = nextNode.y - radius * math.sin(newAng)
                                dev = None
                                if (currSerDev.resistance == 0): #if this current device is a wire
                                    dev = WireSchematic(x0, y0, x1, y1)
                                    dev.refactorDevice()
                                    app.allSchematics.append([dev, None])
                                else: #if this device is a resistor
                                    dev = ResistorSchematic(x0, y0, x1, y1, currSerDev.resistance)
                                    dev.refactorDevice()
                                    rImage = app.schematicToImage(dev)
                                    app.allSchematics.append([dev, rImage])
                                nextNode.combineNodes(dev.getNode1())
                                if (k == len(eachDevInBranch.allDevices) - 1):
                                    paralEndNode = dev.getNode2()
                                nextNode = dev.getNode2()
                    startAng += dAng
                currNode = paralEndNode                        

    def mousePressed(app, event):
        if (not app.isReady):
            app.defineBattery()
            app.isReady = True
            return
        index = 0
        for index in range(len(app.allSchematics)): #checks each node
            eachDevice = app.allSchematics[index][0]
            currentNode1 = eachDevice.getNode1()
            currentNode2 = eachDevice.getNode2()
            if (app.dist(event.x, event.y, currentNode1.x, currentNode1.y) <= Node.nodeWidth):
                app.selectedNode = (index, 1)
                
                if (currentNode1.numConnected() > 0):
                    app.isConnectedNode = True

                return
            elif (app.dist(event.x, event.y, currentNode2.x, currentNode2.y) <= Node.nodeWidth):
                app.selectedNode = (index, 2)
                if (currentNode2.numConnected() > 0):
                    app.isConnectedNode = True
                return

    @staticmethod
    def dist(x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1  - y2) ** 2) ** 0.5
    
    def mouseDragged(app, event):
        if (app.selectedNode != None): #if there is a selected node
            app.showCircAnalysis = False

            (i, num) = app.selectedNode
            movingDevice = app.allSchematics[i][0]
            
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
            
            if (app.isConnectedNode):
                currNode.removeDevice(movingDevice)
                movingDevice.setToNewNode(num)

                app.isConnectedNode = False
                
            # if the 2 nodes are too close to each other, stop moving
            if (app.dist(event.x, event.y, oppositeNodeX, oppositeNodeY) <= movingDevice.height):
                if (not isinstance(movingDevice, WireSchematic)):
                    app.allSchematics[i][1] = app.schematicToImage(movingDevice)
                    movingDevice.calculateCenter()
                    movingDevice.calculateAngle()
                return

            #goes through each schematic and checks if there is a nearby node
            #if so, attach to it
            for index in range(len(app.allSchematics)):
                if (index == i):
                    continue
                eachDevice = app.allSchematics[index][0]
                currentNode1 = eachDevice.getNode1()
                currentNode2 = eachDevice.getNode2()
                if (app.dist(event.x, event.y, currentNode1.x, currentNode1.y) <= Node.nodeWidth * 5):
                    app.connectedNode = currentNode1
                    movingNodeX = currentNode1.x
                    movingNodeY = currentNode1.y
                    break
                elif (app.dist(event.x, event.y, currentNode2.x, currentNode2.y) <= Node.nodeWidth * 5):
                    app.connectedNode = currentNode2
                    movingNodeX = currentNode2.x
                    movingNodeY = currentNode2.y
                    break


            if (num == 1):
                movingDevice.setNode1Pos(movingNodeX, movingNodeY)
            elif (num == 2):
                movingDevice.setNode2Pos(movingNodeX, movingNodeY)
            if (not isinstance(movingDevice, WireSchematic)):
                app.allSchematics[i][1] = app.schematicToImage(movingDevice)
                movingDevice.refactorDevice()
            
    def mouseReleased(app, event):
        app.isConnectedNode = False
        if (app.selectedNode == None):
            return
        
        (i, num) = app.selectedNode
        movingDevice = app.allSchematics[i][0]
        selNode = 0
        oppNode = None

        if (num == 1):
            selNode = movingDevice.getNode1()
            oppNode = movingDevice.getNode2()
        else:
            selNode = movingDevice.getNode2()
            oppNode = movingDevice.getNode1()
        
        if (app.connectedNode != None):
            
            #if the selectedNode and connected node are actually connected
            if (selNode != None and app.connectedNode.x == selNode.x and 
                        app.connectedNode.y == selNode.y):
                app.connectedNode.combineNodes(selNode)
                        
        app.selectedNode = None
    def keyPressed(app, event):
        if (not app.isReady):
            return
        if (event.key == "r"):
            inputRes = app.getUserInput('Input resistance in kilo Ohms')
            if (inputRes == None or not inputRes.isdigit()):
                inputRes = "1"
            r = ResistorSchematic(app.width / 2, 300, app.width / 2, 500, int(inputRes) * 1000)
            i = app.schematicToImage(r)
            app.allSchematics.append([r, i])
        elif (event.key == "s"):
            print()
            print()
            for i in range(len(app.allSchematics)):
                print("current device", app.allSchematics[i][0])
                print("1", app.allSchematics[i][0].getNode1())
                print("2", app.allSchematics[i][0].getNode2())
                print("Node 1", app.allSchematics[i][0].getNode1().getConnectedDevices())
                print("Node 2", app.allSchematics[i][0].getNode2().getConnectedDevices())
                print()
            print()
            print()
        elif (event.key == "Delete"):
            if (len(app.allSchematics) == 1):
                app.app.showMessage("No more devices to delete!")
                return
            deviceToDelete = -1
            currDevice = app.allSchematics[deviceToDelete][0]
            node1 = app.allSchematics[deviceToDelete][0].getNode1()
            node2 = app.allSchematics[deviceToDelete][0].getNode2()
            node1.removeDevice(currDevice)
            node2.removeDevice(currDevice)

            app.allSchematics.pop(deviceToDelete)
        elif (event.key == "w"):
            w = WireSchematic(app.width / 2, 300, app.width / 2, 500)
            app.allSchematics.append([w, None])
        elif (event.key == "c"):
            app.showCircAnalysis = True
            circ = app.schematicsToDevices()
            if (type(circ) == str):
                app.showCircAnalysis = False
                app.app.showMessage(circ)
            else:
                print()
                print(circ)
                print()
                circ.solveCircuit()
        elif (event.key == "R"):
            if (app.app.convertCircuit != None):
                app.app.askVoltage = False
                print(app.app.convertCircuit)
                app.batteryVolt = app.app.convertCircuit.allDevices[0].voltage
                app.deviceToSchematics()
                app.app.convertCircuit = None
            else:
                app.appStarted()
            
        elif (event.key == "S"):
            app.app.convertCircuit = None
            app.app.breadMode.showCircAnalysis = False
            app.app.setActiveMode(app.app.breadMode)

        
    #cannot solve complex circuits at the moment, only 1 parallel layer deep
    def schematicsToDevices(app):
        batterySchematic = app.allSchematics[0][0]
        currNode = batterySchematic.getNode1()
        endNode = batterySchematic.getNode2()

        connectionsInNode = currNode.getConnectedToNode(batterySchematic)
        batteryDevice = batterySchematic.toDevice(None)
        batterySchematic.setDeviceForm(batteryDevice)

        circuit = SeriesDevice(batteryDevice, None)
        priorDevice = batteryDevice

        #while the current node to check is not at the negative side of the battery
        while (currNode != endNode):
            
            if (len(connectionsInNode) == 1): #if the next device is in series
                currSchematic = connectionsInNode[0]
                if (isinstance(currSchematic, BatterySchematic)):
                    return "Disconnected node!"
                currDevice = currSchematic.toDevice(priorDevice, None)
                currSchematic.setDeviceForm(currDevice)
                circuit.addTail(currDevice)
                priorDevice.setTail(currDevice)
                currDevice.setHead(priorDevice)
                priorDevice = currDevice

                if (currSchematic.getNode1() == currNode):
                    currNode = currSchematic.getNode2()
                else:
                    currNode = currSchematic.getNode1()
                connectionsInNode = currNode.getConnectedToNode(currSchematic)
            else: #if the next device is in parallel
                devicesInNode = []
                parallelEndingNode = None
                toExclude = []
                for i in range(len(connectionsInNode)): #iterates through each branch of the parallel node

                    startingSch = connectionsInNode[i]
                    startingDev = startingSch.toDevice(None, None)
                    startingSch.setDeviceForm(startingDev)
                    nextNode = startingSch.getOpposNode(currNode)
                    nextNodeConnections = nextNode.getConnectedToNode(startingSch)
                    currSeriesBranch = SeriesDevice(startingDev, None)

                    lastInBranch = [startingSch]
                    totRes = startingDev.resistance
                    while (True):
                        
                        if (len(nextNodeConnections) == 1): #if the next device is in series
                            if (isinstance(nextNodeConnections[0], BatterySchematic)):
                                return "Disconnected node!"
                            addSeries = nextNodeConnections[0].toDevice(None, None)
                            totRes += addSeries.resistance
                            print("hi")
                            print(addSeries.resistance)
                            nextNodeConnections[0].setDeviceForm(addSeries)
                            currSeriesBranch.addTail(addSeries)
                            lastInBranch = [nextNodeConnections[0]]
                            
                            nextNode = nextNodeConnections[0].getOpposNode(nextNode)
                            nextNodeConnections = nextNode.getConnectedToNode(nextNodeConnections[0])


                            
                        else: #if the next device is in parallel
                            nestedParallelDev = []
                            isSimpleParallel = True
                            if (len(nextNodeConnections) <= 1):
                                return "Disconnected node!"

                            #checks if this parallel node is the end of the current parallel device
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

                    if (len(currSeriesBranch.getAllDevices()) == 1):
                        toExclude.extend([])
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

    def redrawAll(app, canvas):
        canvas.create_text(app.width / 2, 70, text = "Schematic", font = "Arial 60 bold")
        if (not app.isReady):
            canvas.create_text(app.width / 2, app.height / 2, text = "Click to Start!", font = "Arial 60 bold")
            return
        
        #draws each schematic device
        for (schematicDevice, image) in app.allSchematics:

            app.drawDevice(canvas, schematicDevice, image)
            if (type(schematicDevice) == ResistorSchematic):
                canvas.create_text(schematicDevice.cx, schematicDevice.cy, 
                    text = str(schematicDevice.getResistance()) + " Ohms",
                    font = "Arial 12 bold", fill = "red")
            if (schematicDevice.deviceForm != None and app.showCircAnalysis):
                if (schematicDevice.notCompletelyConnected()):
                    continue
                canvas.create_text(schematicDevice.cx, schematicDevice.cy + 15, 
                    text = (str(schematicDevice.deviceForm.voltAcross) + 
                        " V, " + str(schematicDevice.deviceForm.currentAcross) + " mA"),
                    font = "Arial 12 bold", fill = "red")   

    #converts schematic to image
    def schematicToImage(app, schematic):
        image = app.loadImage(schematic.url)
        image = app.scaleImage(image, schematic.scale)
        if (schematic.cropDim != None):
            image = image.crop(schematic.cropDim)
        image = image.rotate(schematic.angle, PIL.Image.NEAREST, expand = 1)
        return image
    
    #draws given schematic
    def drawDevice(app, canvas, schematic, image):
        nodeR = Node.nodeWidth
        node1 = schematic.getNode1()
        node2 = schematic.getNode2()
        (n1X, n1Y, n2X, n2Y) = (node1.x, node1.y, node2.x, node2.y)
        canvas.create_line(n1X, n1Y, n2X, n2Y, width = nodeR, fill = "black")
        canvas.create_oval(n1X - nodeR, n1Y - nodeR, n1X + nodeR, n1Y + nodeR, 
                                                            fill = "white", width = 3)
        canvas.create_oval(n2X - nodeR, n2Y - nodeR, n2X + nodeR, n2Y + nodeR, 
                                                            fill = "white", width = 3)
        if (not isinstance(schematic, WireSchematic)):
            canvas.create_image(schematic.cx, schematic.cy, image=ImageTk.PhotoImage(image))