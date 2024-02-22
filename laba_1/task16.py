def second_largest(numbers):
    #удаляем дубликаты, если они есть
    numbers = list(set(numbers))

    if len(numbers) < 2:
        return None

    #находим максимальное число
    max_num = max(numbers)

    #удаляем максимальное число из списка
    numbers.remove(max_num)

    #находим второе максимальное число
    second_max_num = max(numbers)
    return second_max_num

list1 = [10, 20, 4]
list2 = [70, 11, 20, 4, 100]
print(second_largest(list1))
print(second_largest(list2))
