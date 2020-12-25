#Start Screen for program, includes all the possible controls in this program

from cmu_112_graphics import * # Following framework from cmu_112_graphics
class StartMode(Mode):
    def appStarted(app):
        startPageUrl = "Start Page.jpg"
        # Following picture from https://startupsmagazine.co.uk/article-simplifying-design-process-custom-electronic-circuits
        app.startImage = app.loadImage(startPageUrl)
        app.startImage = app.scaleImage(app.startImage, 2.8)
        app.cx1 = app.width // 4
        app.cx2 = app.width * 0.75
        app.cy1 = app.height * 0.75
        app.cy2 = app.cy1
        app.butHeight = 200
        app.butWidth = 400
    
    def mousePressed(app, event):
        button1Left = app.cx1 - app.butWidth / 2
        button1Right = app.cx1 + app.butWidth / 2
        button1Top = app.cy1 - app.butHeight / 2
        button1Bottom = app.cy1 + app.butHeight / 2
        if (event.x > button1Left and event.x < button1Right and 
                        event.y > button1Top and event.y < button1Bottom):
            app.app.setActiveMode(app.app.schematicsMode)
    
        button2Left = app.cx2 - app.butWidth / 2
        button2Right = app.cx2 + app.butWidth / 2
        button2Top = app.cy2 - app.butHeight / 2
        button2Bottom = app.cy2 + app.butHeight / 2
        if (event.x > button2Left and event.x < button2Right and 
                        event.y > button2Top and event.y < button2Bottom):
            app.app.setActiveMode(app.app.breadMode)

    def redrawAll(app, canvas):
        canvas.create_image(app.width / 2, app.height / 2, image=ImageTk.PhotoImage(app.startImage))
        canvas.create_text(app.width / 2, 70, text = "The Beginners Guide to Schematics and Breadboards", font = "Arial 40 bold", fill = "white")

        shift = 170
        canvas.create_text(app.width / 2, app.height / 2 - shift, 
            text = "Here are controls/options for each of the windows:", 
            font = "Arial 15 bold", fill = "white")
        canvas.create_text(app.width / 2, app.height / 2 + 20 - shift, 
            text = "Press 'r' for creating a new resistor", 
            font = "Arial 15 bold", fill = "white")
        canvas.create_text(app.width / 2, app.height / 2 + 40 - shift, 
            text = "Press 'w' for creating a new wire", 
            font = "Arial 15 bold", fill = "white")
        canvas.create_text(app.width / 2, app.height / 2 + 60 - shift, 
            text = "Press 'c' to solve for the circuit with voltage and current calculations", 
            font = "Arial 15 bold", fill = "white")
        canvas.create_text(app.width / 2, app.height / 2 + 80 - shift, 
            text = "Press 'Delete' to delete the most recent device you inputted", 
            font = "Arial 15 bold", fill = "white")
        canvas.create_text(app.width / 2, app.height / 2 + 100 - shift, 
            text = "Press 'R' to restart that specific mode", 
            font = "Arial 15 bold", fill = "white")
        canvas.create_text(app.width / 2, app.height / 2 + 120 - shift, 
            text = "Press 'S' to switch between modes", 
            font = "Arial 15 bold", fill = "white")
        canvas.create_text(app.width / 2, app.height / 2 + 140 - shift, 
            text = "Click and drag a node to move the device", 
            font = "Arial 15 bold", fill = "white")
        canvas.create_text(app.width / 2, app.height / 2 + 160 - shift, 
            text = "For Schematic Mode, move nodes on top of other nodes to connect them", 
            font = "Arial 15 bold", fill = "white")
        canvas.create_text(app.width / 2, app.height / 2 + 180 - shift, 
            text = "For Breadboard Mode, move nodes to holes on the breadboard to connect them", 
            font = "Arial 15 bold", fill = "white")
        
        canvas.create_text(app.width / 2, app.height / 2 + 60, 
            text = "Start with:", 
            font = "Arial 30 bold", fill = "white")

        canvas.create_rectangle(app.cx1 - app.butWidth / 2, app.cy1 - app.butHeight / 2, 
                        app.cx1 + app.butWidth / 2, app.cy1 + app.butHeight / 2, fill = "orange")
        canvas.create_rectangle(app.cx2 - app.butWidth / 2, app.cy2 - app.butHeight / 2, 
                        app.cx2 + app.butWidth / 2, app.cy2 + app.butHeight / 2, fill = "orange")
        canvas.create_text(app.cx1, app.cy1, 
            text = "Schematics Mode!", 
            font = "Arial 20 bold", fill = "black")
        canvas.create_text(app.cx2, app.cy2, 
            text = "Breadboard Mode!", 
            font = "Arial 20 bold", fill = "black")
    def keyPressed(app, event):
        if (event.key == "s"):
            app.app.setActiveMode(app.app.schematicsMode)
        elif (event.key == "b"):
            app.app.setActiveMode(app.app.breadMode)
#MyApp(width=1500, height=800)