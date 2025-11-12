#1 часть – написать программу в соответствии со своим вариантом задания. 
# Написать 2 варианта формирования (алгоритмический и с помощью функций Питона), сравнив по времени их выполнение.
# 2 часть – усложнить написанную программу, введя по своему усмотрению в условие 
# минимум одно ограничение на характеристики объектов (которое будет сокращать количество переборов) 
# и целевую функцию для нахождения оптимального  решения.
# Вариант 12. Сгенерировать все возможные варианты одномерного массива (К) из чисел 0, 1, 2 и 3. 

import timeit
from itertools import product

def algorithmic_method(K):
    result = [[]]
    for _ in range(K):
        temp = []
        for arr in result:
            for d in (0,1,2,3):
                temp.append(arr + [d])
        result = temp
    return result

def python_method(K):
    return [list(p) for p in product((0,1,2,3), repeat=K)]

def optimized_method(K, max_sum):
    candidates = [list(p) for p in product((0,1,2,3), repeat=K) if sum(p) == max_sum]
    if not candidates:
        return []
    return [arr for arr in candidates if sum(arr) == max_sum]

K = 4
max_sum = 8

alg = algorithmic_method(K)
py = python_method(K)

print("Алг-метод — первые 10 массивов:")
for arr in alg[:10]:
    print(arr)
print("\nPython-метод — первые 10 массивов:")
for arr in py[:10]:
    print(arr)

print(f"\nВсего массивов: {len(py)}\n")

t_alg = timeit.timeit(lambda: algorithmic_method(K), number=100)
t_py  = timeit.timeit(lambda: python_method(K),  number=100)
print(f"Скорость (100 повторов): algorithmic = {t_alg:.4f}s, python = {t_py:.4f}s\n")

optimal = optimized_method(K, max_sum)

print("Оптимальные массивы:")
for i, arr in enumerate(optimal, start=1):  #в массив арр добавляет массив из оптимал а в i добавляет индекс этого массива начиная с 1
    end_char = ", " if i % 5 != 0 and i != len(optimal) else "\n" #указывает что и после каких массивов выводить 
    print(arr, end=end_char)

print(f"\nКоличество оптимальных массивов: {len(optimal)}")
if optimal:
    print("Пример оптимального массива:", optimal[0] , "sum = 8")
