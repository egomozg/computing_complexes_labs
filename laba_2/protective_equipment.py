import short_circuit
import time
import random
import logging

class ProtectiveEquipment():
    def __init__(self, value, probobality_of_failure, op_time_reserve, where):
        self.__value = value
        self.__probobality_of_failure = probobality_of_failure
        self.__op_time_reserve = op_time_reserve
        self.__current = 10
        self.__where = where

    def equipment_operation(self, tok):
        probobality_of_failure = random.randint(0, 100)

        if tok >= self.__value and self.__probobality_of_failure < probobality_of_failure:
            return self.signal_on_switch()
        
        elif tok >= self.__value:
            time.sleep(self.__op_time_reserve / 1000)
            return self.call_reserve_protection()
        
        else:
            logging.info("Значение тока не превышает уставку")
            return False

    # Set Значения тока и сразу его проверяем на срабатывание защиты
    def set_current(self, current):
        self.__current = current
        return self.equipment_operation(self.__current)

    # возвращем значение тока для других видов первичого оборудования
    def get_current(self):
        return self.__current
    
    def set_short_circuit(self):
        return self.set_current(short_circuit.ShortCircuit().get_current())
    
    def signal_on_switch(self):
        logging.info("Произошло короткое замыкание на " + self.__where)
        logging.info ("Сработала основная защита")
        self.__current = 0
        return True
    
    def call_reserve_protection(self):
        logging.info("Произошло короткое замыкание на " + self.__where)
        logging.info("Сработала резервная защита через " + str(self.__op_time_reserve/1000) + " секунды")
        self.__current = 0
        return True