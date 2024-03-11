import protective_equipment
import json
import abstract
import random
import logging 

class Transformer(abstract.abc_perv_ob):
    def __init__ (self, elinput, elout_LV):
        self.__elinput =  elinput 
        self.__elout_LV = elout_LV
        
        with open ('parametri_zashit.json') as param:
            templates = json.load(param)

        self.__protection__HV = protective_equipment.ProtectiveEquipment(templates['setting'], templates['reject_probability'], templates['op_time_reserve'], "Сторона ВН трансформатора")
        self.__protection__LV = protective_equipment.ProtectiveEquipment(templates['setting'], templates['reject_probability'], templates['op_time_reserve'],"Сторона НН трансформатора")
        self.__protection__inside = protective_equipment.ProtectiveEquipment(templates['setting'], templates['reject_probability'], templates['op_time_reserve'], "Внутренняя защита трансформатора")
    
    
    def get_elout(self):
        return self.__elout_LV
    
    def get_elinput(self):
        return self.__elinput
    
    def set_elout(self, elout):
        self.__elout_LV = elout

    def set_elinput(self, elinput):
        self.__elinput = elinput
    
    def set_short_circuit(self):
        arr = [self.__protection__inside, self.__protection__HV, self.__protection__LV]
        per = random.choice(arr) 
        result = per.set_short_circuit()

        if per == self.__protection__inside and result:
            self.__elinput =  None 
            self.__elout_LV = None
            logging.info("Отключены все выключатели")

        elif per == self.__protection__HV and result:
            self.__elinput =  None 
            self.__elout_LV = None
            logging.info("Отключены все выключатели")

        elif per == self.__protection__LV and result:
            self.__elout_LV = None
            logging.info("Отключен выключатель со стороны обмотки НН")
