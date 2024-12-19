'''
С клавиатуры вводится два числа K и N.
Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E заполняется случайным образом целыми числами в интервале [-10,10].
Для тестирования использовать не случайное заполнение, а целенаправленное.

Вариант 5
5.	Формируется матрица F следующим образом: если А симметрична относительно главной диагонали,
то поменять в В симметрично области 1 и 3 местами, иначе С и Е поменять местами несимметрично.
При этом матрица А не меняется. После чего вычисляется выражение: К * (F+A) * A^T – A^T + F.
Выводятся по мере формирования А, F и все матричные операции последовательно.
Вид матрицы A:
E B
D C

Каждая из матриц B,C,D,E имеет вид:    1
                                     4   2
                                       3
'''

import random


# Функция вывода матриц
def print_matrix(matrix):
    for row in matrix:
        print("|", end='')
        for element in row:
            print("{:3}".format(element), end=' ')
        print("|")


def check_matrix_A(matrix):
    for row in range(N):
        for col in range(row + 1, N):
            if matrix[row][col] != matrix[col][row]:
                return False
    return True


# Транспонирование матрицы
def transpose_matrix(matrix, len_matrix):
    # Создаем новую пустую матрицу для хранения результата
    transposed = [[0 for _ in range(len_matrix)] for _ in range(len_matrix)]
    # Транспонируем матрицу
    for i in range(len_matrix):
        for j in range(len_matrix):
            transposed[j][i] = matrix[i][j]
    return transposed


# ================================ №1 Создание основной матрицы A =========================================
# Вводим значения K и N с клавиатуры
K = int(input("Введите размер K: "))

while True:
    N = int(input("Введите размер матрицы N: "))
    if 6 <= N <= 50:
        break
    else:
        print("Ошибка: Размер матрицы должен быть не меньше 6 и не больше 50.")

# Создаем пустую матрицу A(N, N)
matrix_A = [[0 for _ in range(N)] for _ in range(N)]

# Заполняем матрицу A(N, N) случайными числами
for row in range(N):
    for column in range(N):
        matrix_A[row][column] = random.randint(-10, 10)

# Заполняем матрицу для тестирования, размер 10x10. Случай с симметричной матрицой А
K = 5
N = 10
matrix_A = [
    [9, 9, 9, 9, 9, 9, 0, 0, 0, 0],
    [10, 9, 9, 9, 2, 1, 1, 1, 1, 1],
    [9, 9, 9, 9, 2, 2, 2, 2, 2, 2],
    [9, 9, 9, 9, 2, 3, 3, 3, 3, 3],
    [9, 2, 2, 2, 2, 4, 4, 4, 4, 4],
    [9, 1, 2, 3, 4, 4, 4, 4, 4, 4],
    [0, 1, 2, 3, 4, 4, 3, 3, 3, 3],
    [0, 1, 2, 3, 4, 4, 3, 2, 2, 2],
    [0, 1, 2, 3, 4, 4, 3, 2, 1, 1],
    [0, 1, 2, 3, 4, 4, 3, 2, 1, 1]
]

# Определяем размер каждой подматрицы
SIZE_submat = N // 2

# Выводим матрицу A
print("\nМатрица A(N, N):")
print_matrix(matrix_A)

# Создаем и заполняем матрицу F
matrix_F = [[item for item in row] for row in matrix_A]

# Проверка на симметричность матрицы А
if check_matrix_A(matrix_A):
    print("\nМатрица A: симметрична")
    # Создаем и заполняем подматрицу B
    matrix_B = [[0 for _ in range(SIZE_submat)] for _ in range(SIZE_submat)]
    for row in range(SIZE_submat):
        matrix_B[row] = matrix_A[row][SIZE_submat + N % 2:]
    print("\nМатрица B:")
    print_matrix(matrix_B)

    # меняем в В симметрично области 1 и 3 местами
    for row in range(SIZE_submat):
        for column in range(row, SIZE_submat-row):
            matrix_B[row][column], matrix_B[SIZE_submat-1-row][column] = matrix_B[SIZE_submat-1-row][column], matrix_B[row][column]

    print("\nМатрица B после замены областей 1 и 3:")
    print_matrix(matrix_B)
    for row in range(SIZE_submat):
        matrix_F[row][SIZE_submat + N % 2:] = matrix_B[row]

else:
    print("\nМатрица A: несимметрична")
    # меняем С и Е местами несимметрично
    for row in range(SIZE_submat):
            matrix_F[row][:SIZE_submat], matrix_F[row + SIZE_submat + N % 2][SIZE_submat + N % 2:] = \
                matrix_F[row + SIZE_submat + N % 2][SIZE_submat + N % 2:], matrix_F[row][:SIZE_submat]

print("\nМатрица F после всех изменений: ")
print_matrix(matrix_F)


# ================================ №2 Матричные операции =========================================
# К * (F+A) * A^T – A^T + F
print("\nСумма F+A: ")
sum_FA = [[0 for _ in range(N)] for _ in range(N)]
for row in range(N):
    for column in range(N):
        sum_FA[row][column] = matrix_A[row][column] * matrix_F[row][column]
print_matrix(sum_FA)

print("\nПроизведение K * (F + A): ")
mult_KAF = [[0 for _ in range(N)] for _ in range(N)]
for row in range(N):
    for column in range(N):
        mult_KAF[row][column] = sum_FA[row][column] * K
print_matrix(mult_KAF)

print("\nТранспонирование матрицы (A^T): ")
trans_A = transpose_matrix(matrix_A, N)
print_matrix(trans_A)

print("\nПроизведение К * (F+A) * A^T: ")
mult_KAF_AT = [[0 for _ in range(N)] for _ in range(N)]
for row in range(N):
    for column in range(N):
        for k in range(N):
            mult_KAF_AT[row][column] = mult_KAF[row][k] * trans_A[k][column]
print_matrix(mult_KAF_AT)


print("\nРазность матриц К * (F+A) * A^T – A^T: ")
dif_matrix = [[0 for _ in range(N)] for _ in range(N)]
for row in range(N):
    for column in range(N):
        dif_matrix[row][column] = mult_KAF_AT[row][column] - trans_A[row][column]
print_matrix(dif_matrix)


print("\nИтоговый результат К * (F+A) * A^T – A^T + F: ")
end_result = [[0 for _ in range(N)] for _ in range(N)]
for row in range(N):
    for column in range(N):
        end_result[row][column] = dif_matrix[row][column] + matrix_F[row][column]

for row in end_result:
    print("|", end='')
    for element in row:
        print("{:5}".format(element), end=' ')
    print("|")
print("")

