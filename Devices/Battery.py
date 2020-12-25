#Sub class of Device, defines a Battery

from Device import *
class Battery(Device):
    def __init__(self, tail, voltage):
        super().__init__(None, tail)
        if (not isinstance(voltage, int) or voltage <= 0):
            print(voltage)
            print("incompatible types or negative voltage")
            assert(False)
        self.voltage = voltage

    def strForm(self):
        return str(self.voltage) + " V battery"
    
    def __repr__(self):
        return self.strForm()