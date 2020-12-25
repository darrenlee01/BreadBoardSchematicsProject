#runs the application

from BreadBoardMode import *
from SchematicsMode import *
from StartMode import *
from cmu_112_graphics import * # Following framework from cmu_112_graphics

class MyModalApp(ModalApp):
    def appStarted(app):
        app.startMode = StartMode()
        app.breadMode = BreadBoardMode()
        app.schematicsMode = SchematicsMode()
        app.setActiveMode(app.startMode)
        app.convertCircuit = None
        app.askVoltage = True

app = MyModalApp(width=1500, height=800)