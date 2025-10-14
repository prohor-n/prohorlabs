# a1-верхний треугольник а2-правый ф3-нижний а4-левый
#Формируется матрица F следующим образом: Скопировать в нее матрицу А и если количество четных чисел в нечетных столбцах
# в области а1 больше, чем сумма чисел в нечетных строках в области а4, то поменять симметрично области а1 и а4 местами,
# иначе а1 и а2 поменять местами несимметрично. При этом матрица А не меняется. После чего вычисляется выражение: 
# A*А– K*AT. Выводятся по мере формирования А, F и все матричные операции последовательно.
from math import prod

def read_matrix(filename): return [list(map(int, line.split())) for line in open(filename)]
def print_matrix(m, name): print(f"\n{name}:"); [print(" ".join(f"{x:4}" for x in row)) for row in m]
def transpose(m): return [list(row) for row in zip(*m)]

def get_diagonal_regions(n):
    a1, a2, a3, a4 = [], [], [], []
    for i in range(n):
        for j in range(n):
            if i < j and i + j < n - 1: a1.append((i, j))
            elif i < j and i + j > n - 1: a2.append((i, j))
            elif i > j and i + j > n - 1: a3.append((i, j))
            elif i > j and i + j < n - 1: a4.append((i, j))
    return a1, a2, a3, a4

def build_F(A):
    n = len(A)
    F = [row[:] for row in A]
    a1, a2, _, a4 = get_diagonal_regions(n)

    even_in_odd_cols = sum(1 for i, j in a1 if j % 2 == 1 and A[i][j] % 2 == 0)
    sum_odd_rows = sum(A[i][j] for i, j in a4 if i % 2 == 1)

    if even_in_odd_cols > sum_odd_rows:
        for (i1, j1), (i4, j4) in zip(a1, a4):
            F[i1][j1], F[i4][j4] = F[i4][j4], F[i1][j1]
    else:
        for (i1, j1), (i2, j2) in zip(a1, a2):
            F[i1][j1], F[i2][j2] = F[i2][j2], F[i1][j1]

    return F, even_in_odd_cols, sum_odd_rows

def compute_result(A, F, K):
    n = len(A)
    A_T = transpose(A)
    F_T = transpose(F)

    AA = [[sum(A[i][k] * A[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    KF_T = [[K * F_T[i][j] for j in range(n)] for i in range(n)]
    return [[AA[i][j] - KF_T[i][j] for j in range(n)] for i in range(n)]

K = int(input("Введите K: "))
A = read_matrix("matrix.txt")
F, even_count, sum_odd_rows = build_F(A)
R = compute_result(A, F, K)

print_matrix(A, "Исходная матрица A")
print(f"\nЧётных в нечётных столбцах области 1: {even_count}")
print(f"Сумма элементов в нечётных строках области 4: {sum_odd_rows}")
print_matrix(F, "Матрица F после преобразования")
print_matrix(R, "Результат выражения A*A - K*F^T")
