#Sub class of Device, defines a Wire

from Device import *
class Wire(Device):
    def __init__(self, head, tail):
        super().__init__(head, tail)

    def strForm(self):
        return "Wire connecting " + head.strForm() + " to " + tail.strForm()
    
    def __repr__(self):
        return self.strForm()