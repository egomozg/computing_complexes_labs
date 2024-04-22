import json
from Fabric import Fabric
import numpy as np
import matplotlib.pyplot as plt

with open('schema_RL.json') as param: # открываем json файл 
    templates = json.load(param)  # и достаем от туда все

time_of_modeling = templates['time_of_modeling'] #как словарь
step = templates['step']
elements = [Fabric.serialize(elems, step) for elems in templates['elems']] #массив из элементов обращаясь к Fabric ,открывает доступ к elems , шаг расчета
elements_number = len(elements)

nodes = [] #иницализация массива, для хранения узлов

for element in elements:
    if element.get_node_start() not in nodes: #если узла начала нет , то добавляю
        nodes.append(element.get_node_start())
    if element.get_node_end() not in nodes: #если узла конца нет , то добавляю 
        nodes.append(element.get_node_end())

nodes = tuple(sorted(nodes)) #кортеж создаю

matrixA = np.eye((len(nodes) - 1), elements_number)  # np.eye создает матрицу с единицами по диагонали

# Fill matrixA
for i in range(len(nodes) - 1):
    for j in range(elements_number):
        if elements[j].get_node_end() == i + 1:
            matrixA[i][j] = 1
        elif elements[j].get_node_start() == i + 1:
            matrixA[i][j] = -1
        else:
            matrixA[i][j] = 0

# создаем транспонируемую матрицу
matrixAt = np.transpose(matrixA)

# создаем matrix Y (проводимостей)

matrixY = np.eye(elements_number, elements_number)

for i, element in enumerate(elements):
    matrixY[i][i] = (1 / (element.get_impedance()))

# создаем матрицу E
matrixE = np.zeros(elements_number)
matrixE = matrixE[:, np.newaxis] #вектор стоблец делает

def set_matrixE(matrixE, elements, quantity, t):
    for i in range(quantity):
        matrixE[i][0] = elements[i].get_volt(t)
    return matrixE

matrixJ = np.zeros(elements_number)

for i in range(elements_number):
    matrixJ[i] = elements[i].get_current()

matrixJ = matrixJ[:, np.newaxis]

def calculate(matrixA, matrixAt, matrixY, matrixE, matrixJ):
    matrixAY = np.dot(matrixA, matrixY) # перемножение
    matrixAYAt = np.dot(matrixAY, matrixAt)
    matrixYE = np.dot(matrixY, matrixE)
    matrixJ_YE = matrixJ + matrixYE
    matrix_minus_A = (-1) * matrixA 
    marixA_J_YE = np.dot(matrix_minus_A, matrixJ_YE)

    return np.linalg.solve(matrixAYAt, marixA_J_YE)

def set_new_fi(uzl, quantity, elems, Fi):
    for j in range(len(uzl) - 1):
        for i in range(quantity):
            if elems[i].get_node_start() == j + 1:
                elems[i].set_fi_start(Fi[j][0])
            elif elems[i].get_node_end() == j + 1:
                elems[i].set_fi_end(Fi[j][0])
            elif elems[i].get_node_start() == uzl[len(uzl) - 1]:
                elems[i].set_fi_start(0)
            elif elems[i].get_node_end() == uzl[len(uzl) - 1]:
                elems[i].set_fi_end(0)

def set_new_param(quantity, elems):
    for i in range(quantity):
        elems[i].set_current()
        elems[i].set_volt()

array_of_circuits = [0]
array_of_times = [0]
array_of_volt = [0]
time = 0


while (time < time_of_modeling):
    matrixE = set_matrixE(matrixE, elements, elements_number,time)
    matrixFi = calculate(matrixA, matrixAt, matrixY, matrixE, matrixJ)
    set_new_fi(nodes, elements_number, elements, matrixFi)
    set_new_param(elements_number, elements)
    array_of_volt.append(elements[1].get_volt_for_graph())
    array_of_times.append(time)
    array_of_circuits.append(elements[1].get_current_for_graph())
    time += step

plt.plot(array_of_times, array_of_circuits, label="I(t)")
plt.plot(array_of_times, array_of_volt, label="U(t)")
plt.ylabel('Ток,А / Напряжение, В')
plt.xlabel('Время, с')
plt.legend()
plt.minorticks_on()
plt.show()
