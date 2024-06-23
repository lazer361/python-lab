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

count_zero_elements = 0  # Кол-во нулевых элементов
count_negative_elements = 0  # кол-во отрицательных элементов
# Вводим два числа K и N
K = int(input("Введите число K: "))
N = int(input("Введите число N: "))
# Примечание! Т.к в ТЗ, матрица состоит из 4-х равных по размерам под матриц следует что N % 2 == 0 и N >= 6

middle_line = N // 2  # Размерность под матрицы D, E, C, B и средняя линия

#Умножение матриц
def multiply_matrix(m1, m2):
    return [
        [sum(x * y for x, y in zip(m1_r, m2_c)) for m2_c in zip(*m2)] for m1_r in m1
    ]

#Вывод матриц
def print_matrix(arr):
    for i in range(len(arr)):
        for j in range(len(arr)):
            print("{:5d}".format(arr[i][j]), end="")
        print()


# Создаем матрицу A NxN и заполняем ее вручную
print("Матрица A:")
A = [[random.randint(-10, 10) for i in range(N)] for j in range(N)]
for i in range(N):
    for j in range(N):
        A[i][j] = random.randint(-3, 3)
        print("{:4d}".format(A[i][j]), end="")
    print()

D = [[A[i][j] for j in range(N // 2)] for i in range(N//2)]
E = [[A[i][j] for j in range(N // 2, N)] for i in range(0, N//2)]
C = [[A[i][j] for j in range(N // 2)] for i in range(N//2, N)]
B = [[A[i][j] for j in range(N // 2, N)] for i in range(N//2, N)]

F = [[A[i][j] for j in range(N)] for i in range(N)] # Матрица F, при этом матрица А не меняется

# Работаем с E - область 4
for i in range(0, middle_line // 2): #0 3
    for j in range(i+1, (middle_line - i)-1): # 6 12
        if j % 2 == 0 and E[i][j] == 0:
            count_zero_elements += 1
print("Кол-во нулевых элементов в нечётных столбцах: ", count_zero_elements)

# Работаем с E - область 1
for j in range(middle_line - 1, (middle_line // 2), -1):  # [8;5]  8 7 6 5
    for i in range(middle_line - j, middle_line - (middle_line - j)):
        if i % 2 != 0 and E[i][j] < 0:
            count_negative_elements += 1
print("Кол-во отрицательных элементов в чётных строках: ", count_negative_elements)

# Основная часть лаб. Работы
if count_zero_elements > count_negative_elements: # меняем в B симметрично области 4 и 3 местами
    print("Кол-во нулевых элементов в нечётных столбцах БОЛЬШЕ, чем Кол-во отрицательных элементов в чётных строках ")
    # Работаем с матрицей B
    for i in range(0, middle_line // 2):  # 0 3
        for j in range(i + 1, (middle_line - i) - 1):  # 6 12
            # print(i, j)
            B[i][j], B[j][i] = B[j][i], B[i][j]
else:  # меняем B и E местами несимметрично
    print("Кол-во нулевых элементов в нечётных столбцах МЕНЬШЕ, чем Кол-во отрицательных элементов в чётных строках ")
    B, E = E, B

# Собираю матрицу F из D C E B

for i in range(N // 2):
    for j in range(N // 2):
        F[i][j] = D[i][j]  # D

for i in range(N // 2):
    for j in range(N // 2, N):
        F[i][j] = E[i][j - (N // 2)]  # E

for i in range(N // 2, N):
    for j in range(N // 2):
        F[i][j] = C[i - N // 2][j]  # C

for i in range(N // 2, N):
    for j in range(N // 2, N):
        F[i][j] = B[i - N // 2][j - N // 2]  # B

print("Матрица F: ") # новая сформированная матрица F
print_matrix(F)

# Матрицы

AT = [[random.randint(0, 0) for i in range(N)] for j in range(N)]
KF = [[random.randint(0, 0) for i in range(N)] for j in range(N)]
F_plus_A = [[random.randint(0, 0) for i in range(N)] for j in range(N)]
FA_KF = [[random.randint(0, 0) for i in range(N)] for j in range(N)]
FA_KF_AT = [[random.randint(0, 0) for i in range(N)] for j in range(N)]
# Суммирую две матрицы
for i in range(N):
    for j in range(N):
        F_plus_A[i][j] = F[i][j] + A[i][j]
print("Матрица F+A: ")

print_matrix(F_plus_A)

for i in range(N):
    for j in range(N):
        KF[i][j] = K * F[i][j]

print("Матрица KF: ")

print_matrix(KF)

for i in range(N):
    for j in range(N):
        FA_KF[i][j] = F_plus_A[i][j] - KF[i][j]

print("Матрица (F+A)-(K*F): ")
print_matrix(FA_KF)

for i in range(N):
    for j in range(N):
        AT[i][j] = A[j][i]


print("Матрица AT: ") # Транспанированная матрица A
print_matrix(AT)
print("Матрица ((F+A)– (K * F) )*AT : ")
FA_KF_AT = multiply_matrix(FA_KF, AT)
print_matrix(FA_KF_AT)