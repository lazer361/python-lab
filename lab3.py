"""
С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E
заполняется случайным образом целыми числами в интервале [-10,10].
Для тестирования использовать не случайное заполнение, а целенаправленное.

Вид матрицы А:
Е	В
D	С

Для простоты все индексы в подматрицах относительные. Библиотечными методами пользоваться нельзя.
По сформированной матрице F (или ее частям) необходимо вывести не менее 3 разных графиков.

5 Вариант.	Формируется матрица F следующим образом: если в Е количество нулевых элементов в нечетных столбцах в области 4 больше,
чем количество отрицательных элементов в четных строках в области 1, то поменять в В симметрично области 4 и 3 местами,
иначе В и Е поменять местами несимметрично. При этом матрица А не меняется.
После чего вычисляется выражение: ((F+A)– (K * F) )*AT .
Выводятся по мере формирования А, F и все матричные операции последовательно.
"""

import random

K = int(input("Введите K: "))
while True:
    N = int(input("Введите размер/ранг матрицы (N): "))
    if N >= 6 and N % 2 == 0:
        break
    else:
        print(
            "Пожалуйста, введите размер/ранг матрицы (N) число больше/равно 6 и четное число для равных по размеру подматриц")
submatrix_size = N // 2

# Создание подматриц
E = [[random.randint(-10, 10) for _ in range(submatrix_size)] for _ in range(submatrix_size)]
B = [[random.randint(-10, 10) for _ in range(submatrix_size)] for _ in range(submatrix_size)]
D = [[random.randint(-10, 10) for _ in range(submatrix_size)] for _ in range(submatrix_size)]
C = [[random.randint(-10, 10) for _ in range(submatrix_size)] for _ in range(submatrix_size)]

# Создание матрицы A
A = [E[i] + B[i] for i in range(submatrix_size)] + [D[i] + C[i] for i in range(submatrix_size)]
print("Матрица A:")
for row in A:
    print(row)

# Подсчет нулей в нечетных столбцах E
zero_count = 0
for i in range(submatrix_size):
    for j in range(submatrix_size):
        if (j % 2) == 1 and E[i][j] == 0:
            zero_count += 1

# Подсчет отрицательных элементов в четных строках E
negative_count = 0
for i in range(submatrix_size):
    for j in range(submatrix_size):
        if (i % 2) == 0 and E[i][j] < 0:
            negative_count += 1

# Создание матрицы F
F = [E[i] + B[i] for i in range(submatrix_size)] + [D[i] + C[i] for i in range(submatrix_size)]
print("Матрица F:")
for row in F:
    print(row)

# Обмен областей в F
if zero_count > negative_count:
    for i in range(submatrix_size, N):
        for j in range(submatrix_size):
            temp = F[i][j]
            F[i][j] = F[i - submatrix_size][j + submatrix_size]
            F[i - submatrix_size][j + submatrix_size] = temp
else:
    for i in range(submatrix_size):
        for j in range(submatrix_size):
            temp = F[i][j]
            F[i][j] = F[i + submatrix_size][j]
            F[i + submatrix_size][j] = temp

print("Матрица F после преобразования:")
for row in F:
    print(row)

# Транспонирование матрицы A
AT = [[0 for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        AT[j][i] = A[i][j]
print("Транспонированная матрица A (AT):")
for row in AT:
    print(row)

# Сложение матриц F и A
FA = [[0 for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        FA[i][j] = F[i][j] + A[i][j]
print("F + A:")
for row in FA:
    print(row)

# Умножение матрицы F на K
K_F = [[K * element for element in row] for row in F]
print("K * F:")
for row in K_F:
    print(row)

# Вычитание K_F из FA
FA_K_F = [[0 for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        FA_K_F[i][j] = FA[i][j] - K_F[i][j]
print("F + A - K * F:")
for row in FA_K_F:
    print(row)

# Умножение FA_K_F на AT
result = [[0 for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        for k in range(N):
            result[i][j] += FA_K_F[i][k] * AT[k][j]
print("((F + A) - (K * F)) * AT:")
for row in result:
    print(row)
