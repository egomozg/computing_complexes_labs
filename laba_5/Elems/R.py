from Elems import elem_class


class Resistance(elem_class.SuperClass):
    def __init__(self, el, h):
        super().__init__(el, h)
        self.impedance = el['Impedance']

    #def set_volt(self):
    #    self.volt = self.current * self.impedance
