class SuperClass:
    def __init__(self, el, h):
        self.node_start = el['node_start']
        self.node_end = el['node_end']
        self.number_of_branch = el['number_of_branch']
        self.circuit = 0
        self.impedance = 0
        self.current = 0
        self.fi_start = 0
        self.fi_end = 0
        self.volt = 0

    def get_impedance(self):
        return self.impedance

    def get_current(self):
        return self.current

    def get_circuit(self):
        return self.circuit

    def get_volt(self,t):
        return self.volt

    def get_node_start(self):
        return self.node_start

    def get_node_end(self):
        return self.node_end

    def get_fi_start(self):
        return self.fi_start

    def get_fi_end(self):
        return self.fi_end

    def get_current(self):
        return self.current

    def get_volt_for_graph(self):
        return self.volt

    def get_current_for_graph(self):
        return self.current

    # Setters
    def set_fi_start(self, fi_start):
        self.fi_start = fi_start

    def set_fi_end(self, fi_end):
        self.fi_end = fi_end

    def set_current(self):
        self.current = (self.fi_start - self.fi_end) / self.impedance

    def set_volt(self):
        pass
