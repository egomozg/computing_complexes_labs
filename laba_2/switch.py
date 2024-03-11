class Switch():
    
    def __init__(self, name, elinput = 10, elout = 10):
        self.__name = name
        self.__elinput = elinput
        self.__elout = elout
        #self.__mesto_raspolozhinita = mesto_raspolozhinita
        

    def off(self):
        self.__elout = None

    # get and set
    def get_elinput(self):
        return self.__elinput
    
    def get_elout(self):
        return self.__elout

    def set_elinput(self, elinput):
        self.__in = elinput
    
    def set_elout(self, elout):
        self.__out = elout

    def get_name(self):
        return self.__name