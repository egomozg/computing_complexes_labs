from abc import ABC, abstractmethod

class abc_perv_ob(ABC):
    def __init__(self):
        super.__init__(self)

    @abstractmethod
    def get_elinput(self):
        pass

    @abstractmethod
    def get_elout(self):
        pass
    
    @abstractmethod
    def set_elinput(self):
        pass

    @abstractmethod
    def set_elout(self):
        pass

    @abstractmethod
    def set_short_circuit(self):
        pass