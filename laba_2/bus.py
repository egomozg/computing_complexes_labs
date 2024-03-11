import protective_equipment
import json
import abstract
import logging 

class Bus(abstract.abc_perv_ob):   
    def __init__(self, switch, storona):
        self.__switch = switch
        self.__storona = storona
        
        with open('parametri_zashit.json') as param:
            templates = json.load(param)
        self.protection = protective_equipment.ProtectiveEquipment(templates['setting'], templates['reject_probability'], templates['op_time_reserve'], "Защита шины на стороне " + str(self.__storona))
        

    def get_elout(self):
        return self.__elout1
    
    def get_elinput(self):
        arr = [self.__elinput1, self.__elinput2]
        return arr
    
    def set_elout(self, elout1):
        self.__elout1 = elout1

    def set_elinput(self, elinput1, elinput2):
        self.__elinput1 = elinput1
        self.__elinput2 = elinput2

    # def set_short_circuit(self):
    #     if (self.protection.set_short_circuit()):
    #         self.__vvod = None 
    #         self.__vivod1 = None
    #         self.__vivod2 = None
    #         logging.info("Отключены все выключатели присоединенные к шине")

    def set_short_circuit(self):
        if self.protection.set_short_circuit():
            s = "Отключены все выключатели присоединенные к шине: "
            for i in self.__switch:
                i.off()
                s += i.get_name() + ' '
            logging.info(s)