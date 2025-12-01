#Требуется для своего варианта второй части л.р. №5 (усложненной программы) 
# разработать реализацию с использованием графического интерфейса. Допускается 
# использовать любую графическую библиотеку питона. Рекомендуется использовать внутреннюю библиотеку питона  tkinter.
#В программе должны быть реализованы минимум одно окно ввода, одно окно вывода (со скролингом), одно текстовое поле, одна кнопка.

#Сгенерировать все возможные варианты одномерного массива (К) из чисел 0, 1, 2 и 3
#усложнить написанную программу, введя по своему усмотрению в условие 
# минимум одно ограничение на характеристики объектов (которое будет сокращать количество переборов) 
# и целевую функцию для нахождения оптимального  решения.

import math
from itertools import product
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

def optimized_method(K, max_sum):
    candidates = [list(p) for p in product((0,1,2,3), repeat=K) if sum(p) <= max_sum]
    if not candidates:
        return [], 0
    max_s = max(sum(arr) for arr in candidates)
    optimal = [arr for arr in candidates if sum(arr) == max_s]
    return optimal, max_s

def run():
    try:
        K = int(entry_K.get())
        max_sum = int(entry_max.get())
    except ValueError:
        output.insert(tk.END, "Ошибка: введите целые числа для K и ограничения.\n")
        return
    
    ms= 18//K
    optimal, max_s = optimized_method(K, max_sum)
    output.delete("1.0", tk.END)
    output.insert(tk.END, f"Оптимальные массивы (sum = {max_s}):\n")
    for i, arr in enumerate(optimal, start=1):
        end_char = ", " if i % ms != 0 and i != len(optimal) else "\n"
        output.insert(tk.END, f"{arr}{end_char}")
    output.insert(tk.END, f"\nКоличество оптимальных массивов: {len(optimal)}")

root = tk.Tk() #создает окно
root.title("Генерация массивов (Python-метод)")

frm = ttk.Frame(root, padding=10)
frm.grid(row=0, column=0, sticky="ew")

ttk.Label(frm, text="Длина массива K:").grid(row=0, column=0, sticky="w")
entry_K = ttk.Entry(frm, width=10)
entry_K.grid(row=0, column=1, padx=5, sticky="w")
entry_K.insert(0, "4")

ttk.Label(frm, text="Ограничение max_sum:").grid(row=1, column=0, sticky="w")
entry_max = ttk.Entry(frm, width=10)
entry_max.grid(row=1, column=1, padx=5, sticky="w")
entry_max.insert(0, "8")

btn = ttk.Button(frm, text="Запустить", command=run)
btn.grid(row=2, column=0, columnspan=2, pady=5)

output = ScrolledText(root, width=60, height=20, wrap=tk.WORD)
output.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()
