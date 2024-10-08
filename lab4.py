"""
С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц,
B,C,D,E заполняется случайным образом целыми числами в интервале [-10,10].
Для отладки использовать не случайное заполнение, а целенаправленное.

Вид матрицы А:
Е	В
D	С

Для простоты все индексы в подматрицах относительные.
По сформированной матрице F (или ее частям) необходимо вывести не менее 3 разных графиков.
Программа должна использовать функции библиотек numpy  и mathplotlib


5 Вариант.	Формируется матрица F следующим образом: скопировать в нее А и если А симметрична относительно главной
диагонали, то поменять местами С и  В симметрично, иначе С и Е поменять местами несимметрично.
При этом матрица А не меняется.
После чего если определитель матрицы А больше суммы диагональных элементов матрицы F, то вычисляется выражение:
A-1*AT – K * F-1, иначе вычисляется выражение (AТ +G-FТ)*K, где G-нижняя треугольная матрица, полученная из А.
Выводятся по мере формирования А, F и все матричные операции последовательно.
"""

import numpy as np
import matplotlib.pyplot as plt
import random

# Ввод размеров матрицы
K = int(input("Введите K: "))
N = int(input("Введите N: "))

# Проверка на четность N
if N % 2 != 0:
    print("N должно быть четным числом!")
    exit()

# Размер подматриц
submatrix_size = N // 2

# Целенаправленное заполнение подматриц
# Для проверки используйте следующие значения:
# E = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
# B = [[17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]]
# D = [[33, 34, 35, 36], [37, 38, 39, 40], [41, 42, 43, 44], [45, 46, 47, 48]]
# C = [[49, 50, 51, 52], [53, 54, 55, 56], [57, 58, 59, 60], [61, 62, 63, 64]]

# E = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
# B = [[17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]]
# D = [[33, 34, 35, 36], [37, 38, 39, 40], [41, 42, 43, 44], [45, 46, 47, 48]]
# C = [[49, 50, 51, 52], [53, 54, 55, 56], [57, 58, 59, 60], [61, 62, 63, 64]]

E = np.array([[random.randint(-10, 10) for _ in range(submatrix_size)] for _ in range(submatrix_size)])
B = np.array([[random.randint(-10, 10) for _ in range(submatrix_size)] for _ in range(submatrix_size)])
D = np.array([[random.randint(-10, 10) for _ in range(submatrix_size)] for _ in range(submatrix_size)])
C = np.array([[random.randint(-10, 10) for _ in range(submatrix_size)] for _ in range(submatrix_size)])

# Создание матрицы A
A = np.concatenate((np.concatenate((E, B), axis=1), np.concatenate((D, C), axis=1)), axis=0)
print("Матрица A:")
print(A)

# Создание матрицы F
F = A.copy()
print("Матрица F:")
print(F)

# Проверка на симметричность
symmetric = np.allclose(A, A.T)

# Изменение областей в F
if symmetric:
    print("Обмен областей C и B симметрично")
    # Обмен областей C и B симметрично
    F[:submatrix_size, submatrix_size:] = F[submatrix_size:, :submatrix_size].copy()
    F[submatrix_size:, :submatrix_size] = A[:submatrix_size, submatrix_size:].copy()
else:
    print("Обмен областей C и E несимметрично")
    # Обмен областей C и E несимметрично
    F[submatrix_size:, :submatrix_size] = F[:submatrix_size, :submatrix_size].copy()
    F[:submatrix_size, :submatrix_size] = A[submatrix_size:, :submatrix_size].copy()

print("Матрица F после преобразования:")
print(F)

# Вычисление определителя матрицы A
det_A = np.linalg.det(A)
print("Определитель матрицы A:", det_A)

# Вычисление суммы диагональных элементов матрицы F
sum_diag_F = np.trace(F)
print("Сумма диагональных элементов матрицы F:", sum_diag_F)
AT = A.T
# Выбор ветви вычислений
if det_A > sum_diag_F:
    print("det_A > sum_diag_F")
    # Вычисление A-1*AT – K * F-1
    A_inverse = np.linalg.inv(A)
    result = np.dot(A_inverse, AT) - K * np.linalg.inv(F)
else:
    print("det_A <= sum_diag_F")
    # Вычисление (AТ +G-FТ)*K
    G = np.tril(A) # Нижняя треугольная матрица
    FT = F.T
    result = np.dot(AT + G - FT, K)

# Вывод результата
print("Результат:")
print(result)

# Построение графиков
plt.figure(figsize=(12, 4))

# График 1: Гистограмма
plt.subplot(2, 2, 1)
plt.hist(result.flatten(), bins=10)
plt.title('Гистограмма значений результата')

# График 2: Круговая диаграмма
plt.subplot(2, 2, 2)
unique, counts = np.unique(result.flatten(), return_counts=True)
plt.pie(counts, labels=unique, autopct='%1.1f%%')
plt.title('Круговая диаграмма значений результата')

# График 3: Линейная диаграмма
plt.subplot(2, 2, 3)
plt.plot(result.flatten())
plt.title('Линейная диаграмма значений результата')
plt.xlabel('Индекс')
plt.ylabel('Значение')

plt.tight_layout()
plt.show()
