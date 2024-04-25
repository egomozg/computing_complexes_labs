from Elems import elem_class


class J(elem_class.SuperClass):
    def __init__(self, el, h):
        super().__init__(el, h)
        self.impedance = el['Impedance']
        self._current = el['Current']

    def set_current(self):
        self.current = self._current
