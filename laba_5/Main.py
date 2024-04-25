import json
from threading import Thread
import multiprocessing
from Fabric import Fabric
import time
import numpy as np
import matplotlib.pyplot as plt

def scheme_calc(config):
    with open(config) as param: # открываем json файл 
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

    nodes = tuple(sorted(nodes))

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
        array_of_volt.append(elements[2].get_volt_for_graph())
        array_of_times.append(time)
        array_of_circuits.append(elements[2].get_current_for_graph())
        time += step

    print("Схема под названием", config)

    return array_of_times, array_of_circuits, array_of_volt, config

def time_it(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print(f'Время выполнения программы: {((end - start) * 1000)} мс.')
    return wrapper

def plot_functions(array_of_times, array_of_circuits, array_of_volt, config):
    fig, ax = plt.subplots()
    ax.plot(array_of_times, array_of_circuits, label="I(t)")
    ax.plot(array_of_times, array_of_volt, label="U(t)")
    ax.set_ylabel('Ток,А / Напряжение, В')
    ax.set_xlabel('Время, с')
    ax.legend()
    fig.savefig('/home/egorsuse/Documents/smb_share/' + config + '_plot.png')
    print('Fig saved to ~/Documents/smb_share' + config + '_plot.png')


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

@time_it
def thread_calc():
    t1 = ThreadWithReturnValue(target=scheme_calc, args=('schema_RL.json',))
    t2 = ThreadWithReturnValue(target=scheme_calc, args=('schema_RC.json',))
    t3 = ThreadWithReturnValue(target=scheme_calc, args=('schema_RLC.json',))
    t1.start()
    t2.start()
    t3.start()

    t4 = Thread(target=plot_functions, args=(t1.join()))
    t5 = Thread(target=plot_functions, args=(t2.join()))
    t6 = Thread(target=plot_functions, args=(t3.join()))
    t4.start()
    t5.start()
    t6.start()

    t4.join()
    t5.join()
    t6.join()


@time_it
def multiprocessing_calc():
    t1 = multiprocessing.Process(target=scheme_calc, args=('schema_RL.json',))
    t2 = multiprocessing.Process(target=scheme_calc, args=('schema_RC.json',))
    t3 = multiprocessing.Process(target=scheme_calc, args=('schema_RLC.json',))
    
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

@time_it
def non_multithread_calc():
    scheme_calc("schema_RL.json")
    scheme_calc("schema_RC.json")
    scheme_calc("schema_RLC.json")

if __name__ == "__main__":
    thread_calc()
    #non_multithread_calc()
    #multiprocessing_calc()
