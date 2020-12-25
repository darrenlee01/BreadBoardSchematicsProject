#Sub class of Device, Defines a new resistor

from Device import *
class Resistor(Device):
    def __init__(self, head, tail, resistance):
        super().__init__(head, tail)
        if (not isinstance(resistance, int) or resistance < 0):
            print("incompatible types or non positive resistance")
            assert(False)
        self.resistance = resistance
        self.resistanceAcross = resistance

    def strForm(self):
        return str(self.resistance) + " ohm Resistor"
    
    def __repr__(self):
        return self.strForm()