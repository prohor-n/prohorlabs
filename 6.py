#1.	F(n<=5)=10 ; F(n)= ((-1)^n)*(6*F(n-1)-7*F(n-2))/((2n)!)  (при n >12), F(n)=F(n-2)-F(n-1) (при 5<n<=12)
#Область определения функции – натуральные числа. Написать программу сравнительного 
# вычисления данной функции рекурсивно и итерационно (значение, время). 
# вывести таблицу и график сравнения времени рекурсивного и итерационого метода 
import math
import timeit
import matplotlib.pyplot as plt

def F_recursive(n: int) -> float:
    if n <= 5:
        return 10
    elif 5 < n <= 12:
        return (F_recursive(n-2) - F_recursive(n-1))
    else:
        return (((-1)**n) * (6*F_recursive(n-1) - 7*F_recursive(n-2)) / (math.factorial(2*n)))

def F_iterative(n):
    F = {}
    factorial_cache = 1
    for i in range(n+1):
        if i >= 1:
            factorial_cache *= (2*i - 1)*(2*i)
        if i <= 5:
            F[i] = 10
        elif 5 < i <= 12:
            F[i] = F[i-2] - F[i-1]
        else:
            F[i] = ((-1)**i) * (6*F[i-1] - 7*F[i-2]) / factorial_cache
    return F[n]

results = [(n,
            timeit.timeit(lambda n=n: F_recursive(n), number=10),
            timeit.timeit(lambda n=n: F_iterative(n), number=10))
           for n in range(2, 21)]   

print(f"{'n':>3} {'Время рекурсия (с)':>18} {'Время итерация (с)':>18}")
for n, trec, titer in results:
    print(f"{n:>3} {trec:>18.6f} {titer:>18.6f}")

plt.figure(figsize=(8,5))
plt.plot([r[0] for r in results], [r[1] for r in results], '--o', label='Рекурсия')
plt.plot([r[0] for r in results], [r[2] for r in results], '-o', label='Итерация')
plt.xlabel('n')
plt.ylabel('время (с)')
plt.title('Сравнение времени: рекурсия vs итерация')
plt.legend()
plt.grid(True)
plt.show()

plt.grid(True)
plt.show()


