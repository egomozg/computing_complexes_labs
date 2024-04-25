from Elems import elem_class


class EDS(elem_class.SuperClass):
    def __init__(self, el, h):
        super().__init__(el, h)
        self.impedance = el['Impedance']
        self.volt = el['Volt']

    def set_current(self):
        self.current = (self.volt - (self.fi_start - self.fi_end)) / self.impedance

    def set_voltage(self):
        return self.volt
