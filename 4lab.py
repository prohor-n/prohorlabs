#с клавиатуры вводится число K. матрица (N, N) состоящее из четырех равных подматриц E B D C
#Формируется матрица F следующим образом: Скопировать в нее матрицу А
#и если количество четных чисел в нечетных столбцах в области 1 больше
#чем сумма чисел в нечетных строках в области 4, то поменять симметрично области 1 и 4 местами
#иначе 1 и 2 поменять местами несимметрично После чего вычисляется выражение: A*А – K*A^T. 
# Выводятся по мере формирования А, F и все матричные операции последовательно.
# вывести 3 различных графика 
import numpy as np
import matplotlib.pyplot as plt

def load_matrix():
    A = np.loadtxt("matrix_data.txt", dtype=int)
    if A.shape[0] != A.shape[1]: exit("Матрица должна быть квадратной")
    if A.shape[0]%2==1: exit("матрица должна быть четной")
    return A

def build_F(A):
    F, n = A.copy(), A.shape[0] // 2
    E, B, C = A[:n, :n], A[:n, n:], A[n:, n:]
    even_count_in_odd_columns = sum(1 for j in range(0, n, 2) for i in range(n) if E[i, j] % 2 == 0)
    odd_row_sum = np.sum(C[0::2])
    print(f"\nПростых в нечётных столбцах B: {even_count_in_odd_columns}\nСумма чисел в нечётных строках E: {odd_row_sum}")
    if even_count_in_odd_columns > odd_row_sum:
        F[:n, :n], F[:n, n:] = np.fliplr(B), np.fliplr(E)
    else:
        F[:n, :n], F[n:, n:] = C.copy(), E.copy()
    return F

def compute_result(A, K):
    return A @ A - K * A.T

def plot_graphs(F):
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    axs[0].plot(F.sum(axis=1)); axs[0].set_title("Сумма строки"); axs[0].set_xlabel("Номер строки"); axs[0].set_ylabel("Сумма")
    axs[1].bar(range(F.shape[1]), np.mean(F, axis=0)); axs[1].set_title("среднее значение столбца"); axs[1].set_xlabel("Номер столбца"); axs[1].set_ylabel("Среднее значение")
    axs[2].hist(F.flatten(), bins=9); axs[2].set_title("количество цифр в матрице");  axs[2].set_xlabel("цифра"); axs[2].set_ylabel("Количество")
    for ax in axs: ax.grid(True) #добавляет сетку для графиков
    plt.tight_layout(); plt.show()  # подбирает автоматически расстояние между графиками и показывает графики 

def main():
    K = int(input("Введите K: "))
    A = load_matrix(); print("\nA:\n", A)
    F = build_F(A); print("\nF:\n", F)
    R = compute_result(A, K); print("\nРезультат:\n", R)
    plot_graphs(F)

main()
