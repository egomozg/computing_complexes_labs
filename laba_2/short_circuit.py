import random
import math
import logging 

class ShortCircuit():
    def __init__(self, max_current = 3000):
        self.__max_value_3PH = max_current
        self.__max_value_2PH = self.__max_value_3PH * (math.sqrt(3) / 2)
    def get_current(self):
        arr = [random.randint(50, int(self.__max_value_2PH)), random.randint(int(self.__max_value_2PH), self.__max_value_3PH)]
        value = random.choice(arr)
        logging.info("Величина тока КЗ: " + str(value) + " А")
        return value