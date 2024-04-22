import random
from transformer import Transformer 
from switch import Switch
from bus import Bus
from line import Line
import logging 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
# Выключатели четырехугольника РУВН
switch_1 = Switch('Выключатель_1')
switch_2 = Switch('Выключатель_2')
switch_3 = Switch('Выключатель_3')
switch_4 = Switch('Выключатель_4')

#Выключатели на обмотке ВН трансформаторов
switch_HV_1 = Switch('Выключатель_ВН_1')
switch_HV_2 = Switch('Выключатель_ВН_2')

#Шина со стороны вн
bus_1 = Bus([switch_1, switch_2, switch_HV_2], 'ВН')
bus_2 = Bus([switch_3, switch_4, switch_HV_1], 'ВН')

# Выключатели для сторон НН обоих трансформаторов
switch_LV_1 = Switch('Выключатель_НН_1')
switch_LV_2 = Switch('Выключатель_НН_2')

switch_line_1 = Switch('Выключатель_линии_1')

# Трансформаторы
tr_1 = Transformer(switch_HV_1.get_elout(), switch_LV_1.get_elinput())
tr_2 = Transformer(switch_HV_2.get_elout(),switch_LV_2.get_elinput())

# Шина со стороны НН
bus_3 = Bus([switch_LV_1, switch_LV_2, switch_line_1], 'НН')

# Отходяшии линии НН
line_1 = Line(switch_line_1.get_elout(), "Линия №1 (НН)")


oborydovanie = (bus_1, bus_2, bus_3, tr_1, tr_2, line_1)

i = 0
while i < 15:
    i += 1
    logging.info("---------------------------------------------Итерация #"+ str(i) + "-------------------------------------")
    random.choice(oborydovanie).set_short_circuit()
