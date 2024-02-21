"""Задание в лаборатории. Вариант 2. Савченко Егор Э-12-20"""
import math

def replace_elements_based_on_task(arr):
    """Задание 2: увеличивает элементы кратные трем в 4 раза, и на 6 остальные элементы"""
    new_arr = [0] * len(arr)
    for i, x in enumerate(arr):
        if x % 3 == 0:
            new_arr[i] = x * 4
        else:
            new_arr[i] = x + 6
    return new_arr
    #без enumerate (не такая красивая версия)
    #for i in range(len(arr)):
    #    if arr[i] % 3 == 0:
    #        arr[i] *= 4
    #    else:
    #        arr[i] += 6

def dict_combine_set_and_list(key, value):
    """Задание 3: cоздание словаря, где ключ - элемент множества, а значение - списка"""
    some_dict = {}
    for dict_key, dict_value in zip(key, value):
        some_dict[dict_key] = dict_value
    return some_dict

def find_index(arr, y):
    """Возвращает индекс заданного элемента из массива"""
    for x in arr:
        if x == y:
            return arr.index(x)
    return "Элемент не найден"

def filter_dict_by_median(dictionary, keys):
    """Фильтруем словарь по ключам и медиане"""
    # Извлекаем значения по ключам из списка
    values = [0] * len(keys)
    for i, key in enumerate(keys):
        if key in dictionary:
            values[i] = dictionary[key]
        else:
            values.pop(i)

    #values = [dictionary[key] for key in keys if key in dictionary]
    # Вычисляем медиану
    median = sorted(values)[len(values) // 2]
    # Фильтруем словарь по значению и создаем новый словарь
    filtered = list(filter(lambda x: x >= median, values))
    new_dict = {}
    for new_keys, new_values in zip(keys, filtered):
        new_dict[new_keys] = new_values
    return new_dict

def process_numbers(min_val, max_val, step):
    """задание 6"""
    # Генерируем список чисел
    numbers = list(range(min_val, max_val + 1, step))

    # Вычисляем сумму квадратов четных чисел
    even_squares_sum = 0
    for x in numbers:
        if x % 2 == 0:
            even_squares_sum += x**2

    # Вычисляем квадратный корень из суммы
    square_root = math.sqrt(even_squares_sum)

    # Создаем множество нечетных чисел, кратных 3
    odd_multiples_of_three = set()
    for x in numbers:
        if x % 2 != 0 and x % 3 == 0:
            odd_multiples_of_three.update([x])

    return square_root, odd_multiples_of_three

def check_password_strength(my_password):
    """Задание 7"""
    if len(password) < 8:
        return False

    has_upper = False
    has_lower = False
    has_digit = False

    for char in my_password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True

    return has_upper and has_lower and has_digit

# Задание 1: множество список от 1 до 10
some_set = set(range(1,11))
print("Мое множество= ", some_set)

# Задание 2: создаю список из множество и меняю значения
some_list = list(some_set)
mod_list = replace_elements_based_on_task(some_list)
print(mod_list)

# Задание 3
print(some_list)
print(dict_combine_set_and_list(some_list, mod_list))

# Задание 4
print(find_index(some_list, 3))

# Задание 5
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
key_list = ['a', 'b', 'c', 'd', 'e']

result = filter_dict_by_median(d, key_list)
print(result)

# Задание 6
MIN_VALUE = 1
MAX_VALUE = 10
STEP_VALUE = 1

sqrt, odd = process_numbers(MIN_VALUE, MAX_VALUE, STEP_VALUE)
print(sqrt, odd)

# Задание 7
password = input("Введите пароль: ")
if check_password_strength(password):
    print("Пароль надежен.")
else:
    print('''Пароль ненадежен. Он должен содержать не менее 8 символов,
          включая буквы в верхнем и нижнем регистре и одну цифру.''')
