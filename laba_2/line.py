import protective_equipment
import json
import abstract
import random
import logging 

class Line(abstract.abc_perv_ob):
    def __init__ (self, elinput, name):
        self.__elinput = elinput 
        self.__name = name
        
        with open ('parametri_zashit.json') as param:
            tempates = json.load(param)
        self.protection = protective_equipment.ProtectiveEquipment(tempates['setting'],tempates['reject_probability'], tempates['op_time_reserve'], str(self.__name))
        
    def get_elout(self):
        pass
    
    def get_elinput(self):
        return self.__elinput
    
    def set_elout(self, elout):
        self.__elout = elout

    def set_elinput(self, elinput):
        self.__elinput = elinput
    
    def set_short_circuit(self):
        probobality_of_failure = random.randint(0,100)
        if (probobality_of_failure < 50):
            logging.info("КЗ на " + str(self.__name) + " самоустранилось")
        elif (self.protection.set_short_circuit()):
            self.__vvod = None 
            logging.info("Отключен выключатель со стороны шины")