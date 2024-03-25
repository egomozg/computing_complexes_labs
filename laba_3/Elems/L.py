from Elems import elem_class


class L(elem_class.SuperClass):
    def __init__(self, el, h):
        super().__init__(el, h)
        self.impedance = 2 * el['Inductance'] / h
        self.current = el["Current"]
        self.E = 0


    def set_volt(self):
        self.E = (self.impedance * self.current + self.volt)

    def get_volt(self,t):
        return self.E


    def set_current(self):
        self.current = (self.E - (self.fi_start - self.fi_end)) / self.impedance
        self.volt = (self.current * self.impedance - self.E)

    def get_volt_for_graph(self):
        return self.volt