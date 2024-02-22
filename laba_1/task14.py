def even_counter(arr):
    counter = 0
    for x in arr:
        if x % 2 == 0:
            counter += 1
    return counter

list1 = [2, 7, 5, 64, 14]
list2 = [12, 14, 95, 3]

first_even_counter = even_counter(list1)
second_even_counter = even_counter(list2)

# для нахождения нечетных - из количества элементов в списке вычитаем количество четных
print("Even = ", first_even_counter, "odd = ", len(list1) - first_even_counter)
print("Even = ", second_even_counter, "odd = ", len(list2) - second_even_counter)
