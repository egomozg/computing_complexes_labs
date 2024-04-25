from Elems import elem_class


class C(elem_class.SuperClass):
    def __init__(self, el, h):
        super().__init__(el, h)
        self.impedance = (h / ( el['Capacity'])) # without 2
        self.volt = el['Volt']

    def set_volt(self):
        self.volt = self.current * self.impedance + self.volt

    def get_voltage(self,t):
        return self.volt

    def set_current(self):
        self.current = (-self.volt + (self.fi_start - self.fi_end)) / self.impedance

    def get_volt_for_graph(self):
        return -self.volt

    def get_current_for_graph(self):
        return -self.current