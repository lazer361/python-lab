"""
С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E
заполняется случайным образом целыми числами в интервале [-10,10].
Для тестирования использовать не случайное заполнение, а целенаправленное.

Вид матрицы А:
Е	В
D	С

Для простоты все индексы в подматрицах относительные. Библиотечными методами пользоваться нельзя.


5 Вариант.	Формируется матрица F следующим образом: если А симметрична относительно главной диагонали,
то поменять в В симметрично области 1 и 3 местами, иначе С и Е поменять местами несимметрично.
При этом матрица А не меняется. После чего вычисляется выражение: К * (F+A) * AT – AT + F.
Выводятся по мере формирования А, F и все матричные операции последовательно.
"""

import random

# Ввод размеров матрицы
K = int(input("Введите K: "))

while True:
    N = int(input("Введите размер/ранг матрицы (N): "))
    if N >= 6 and N % 2 == 0:
        break
    else:
        print(
            "Пожалуйста, введите размер/ранг матрицы (N) число больше/равно 6 и четное число для равных по размеру подматриц")

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

E = [[random.randint(-10, 10) for _ in range(submatrix_size)] for _ in range(submatrix_size)]
B = [[random.randint(-10, 10) for _ in range(submatrix_size)] for _ in range(submatrix_size)]
D = [[random.randint(-10, 10) for _ in range(submatrix_size)] for _ in range(submatrix_size)]
C = [[random.randint(-10, 10) for _ in range(submatrix_size)] for _ in range(submatrix_size)]

# Создание матрицы A
A = [E[i] + B[i] for i in range(submatrix_size)] + [D[i] + C[i] for i in range(submatrix_size)]
print("Матрица A:")
for row in A:
    print(row)

# Проверка на симметричность
symmetric = True
for i in range(N):
    for j in range(i + 1, N):
        if A[i][j] != A[j][i]:
            symmetric = False
            break
    if not symmetric:
        break

# Формирование матрицы F
F = [E[i] + B[i] for i in range(submatrix_size)] + [D[i] + C[i] for i in range(submatrix_size)]
print("Матрица F:")
for row in F:
    print(row)

# Изменение областей в F
if symmetric:
    print("Обмен областей 1 и 3 в B симметрично")
    # Обмен областей 1 и 3 в B симметрично
    for i in range(submatrix_size):
        for j in range(submatrix_size):
            temp = F[i][j]
            F[i][j] = F[i + submatrix_size][j + submatrix_size]
            F[i + submatrix_size][j + submatrix_size] = temp
else:
    print("Обмен областей C и E несимметрично")
    # Обмен областей C и E несимметрично
    for i in range(submatrix_size):
        for j in range(submatrix_size):
            temp = F[i][j]
            F[i][j] = F[i + submatrix_size][j]
            F[i + submatrix_size][j] = temp

print("Матрица F после преобразования:")
for row in F:
    print(row)

# Сложение матриц F и A
FA = [[0 for _ in range(N)] for _ in range(N)]
print("F + A:")
for i in range(N):
    for j in range(N):
        FA[i][j] = F[i][j] + A[i][j]
        print(FA[i][j], end=" ")
    print()

# Транспонирование матрицы A
AT = [[0 for _ in range(N)] for _ in range(N)]
print("Транспонированная матрица A (AT):")
for i in range(N):
    for j in range(N):
        AT[j][i] = A[i][j]
        print(AT[i][j], end=" ")
    print()

# Умножение матрицы (F+A) на AT
result = [[0 for _ in range(N)] for _ in range(N)]
print("(F + A) * AT:")
for i in range(N):
    for j in range(N):
        for k in range(N):
            result[i][j] += FA[i][k] * AT[k][j]
        print(result[i][j], end=" ")
    print()

# Умножение на K
print("K * (F+A) * AT:")
for i in range(N):
    for j in range(N):
        result[i][j] *= K
        print(result[i][j], end=" ")
    print()

# Вычитание AT
print("- AT:")
for i in range(N):
    for j in range(N):
        result[i][j] -= AT[i][j]
        print(result[i][j], end=" ")
    print()

# Сложение с F
print("+ F:")
for i in range(N):
    for j in range(N):
        result[i][j] += F[i][j]
        print(result[i][j], end=" ")
    print()

print("Результат: К * (F+A) * AT – AT + F:")
for row in result:
    print(row)
