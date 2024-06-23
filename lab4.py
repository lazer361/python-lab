"""
С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E
заполняется случайным образом целыми числами в интервале [-10,10]. Для отладки использовать не случайное заполнение,
а целенаправленное.

Вид матрицы А:
Е	В
D	С

5 Вариант.	Формируется матрица F следующим образом: если в Е количество нулевых элементов в нечетных столбцах в области 4 больше,
чем количество отрицательных элементов в четных строках в области 1, то поменять в В симметрично области 4 и 3 местами,
иначе В и Е поменять местами несимметрично. При этом матрица А не меняется.
После чего вычисляется выражение: ((F+A)– (K * F) )*AT .
Выводятся по мере формирования А, F и все матричные операции последовательно.
"""

import numpy as np
import matplotlib.pyplot as plt
import pylab

K = int(input("Введите число K:"))
N = int(input("Введите число K:"))
M = N // 2
count_zero_elements = 0  # Кол-во нулевых элементов
count_negative_elements = 0  # кол-во отрицательных элементов



print("B")
b = np.random.randint(-10, 10, (M, M))
print(b, '\n')
print("C")
c = np.random.randint(-10, 10, (M, M))
print(c, '\n')
print("D")
d = np.random.randint(-10, 10, (M, M))
print(d, '\n')
print("E")
e = np.random.randint(-10, 10, (M, M))
print(e, '\n')

# Матрица А
print("Матрица A: ")
a = np.vstack(((np.hstack([d, e])), (np.hstack([c, b]))))
print(a)

print()


#  **** Определитель матрицы A
det_A = int(np.linalg.det(a))
print(f"Определитель матрицы A: {det_A}")

# G-нижняя треугольная матрица, полученная из А
g = np.tri(N) * a
print("Матрица G:")
print(g)

# Матрица F
f = a.copy()
print("матрица F")
print(f)

# Кол-во нулевых элементов в матрице E
for i in range(M):
    for j in range(0, M, 2):
        if e[i][j] == 0:
            count_zero_elements += 1
print(f"Кол-во нулевых элементов в матрице E: {count_zero_elements}")


# количество отрицательных элементов в матрице E
for i in range(1, M, 2):
    for j in range(0, M):
        if e[i][j] < 0:
            count_negative_elements += 1
print(f"Количество отрицательных элементов в матрице E: {count_negative_elements}")


if count_zero_elements >= count_negative_elements:
    print("Кол-во нулевых элементов в нечёт.стлбц больше, чем кол-во отрицательных элементов в чётных строках")
    # меняем C и B симметрично
    f[M:N, M:N] = np.fliplr(c)
    f[M:N, :M] = np.fliplr(b)
else:
    # меняем C и B несимметрично
    print("Кол-во нулевых элементов в нечёт.стлбц меньше или равно, чем кол-во отрицательных элементов в чётных строках")
    f = np.vstack(((np.hstack([d, b])), (np.hstack([c, e]))))


# *** Сумма Диагональных элементов
summ_diagonal_elements = sum(np.diagonal(f))
print("Сумма Диагональных элементов:", summ_diagonal_elements)


if det_A > summ_diagonal_elements:
    print("Определитель Матрицы А больше суммы диагональных элементов матрицы F")
    print("A-1")
    print(np.linalg.inv(a))
    print()
    print("A_T")
    print(np.matrix.transpose(a))
    print()
    print("K * F")
    print(K * f)
    print()
    print("A-1 * A_T")
    print((np.linalg.inv(a) * np.matrix.transpose(a)))
    print()
    print("A-1 * A_T - K * F")
    rezult = (np.linalg.inv(a) * np.matrix.transpose(a)) - (K * f)
    print(rezult)
else:
    print("Определитель Матрицы А меньше или равно суммы диагональных элементов матрицы F")
    print("A_T")
    print(np.matrix.transpose(a))
    print()
    print("F-1")
    print(np.linalg.inv(f))
    print()
    print("G - F-1")
    print(g - np.linalg.inv(f))
    print()
    print("A_T + G - F-1")
    print(np.matrix.transpose(a) + g - np.linalg.inv(f))
    print()
    print("(A_T + G - F-1) * K")
    rezult = (np.matrix.transpose(a) + g - np.linalg.inv(f)) * K
    print(rezult)




F3 = f.reshape(-1)
x = list()
for i in range(N):
    for j in range(N):
        x.append(str(i)+str(j))
pylab.subplot(2, 2, 1)
pylab.plot(x, F3, marker='o', markersize=3)
pylab.xlabel('Индекс элемента')
pylab.ylabel('Значение')
pylab.title('Первый график')


pylab.subplot(2, 2, 2)
F4 = np.sort(f, axis=None)

pylab.plot(x, F4, color='red', marker='o', markersize=3)
pylab.xlabel('Индекс элемента')
pylab.ylabel('Значение')
pylab.title('Второй график')


pylab.subplot(2, 2, 3)
F6 = np.max(f, axis=1)
pylab.bar(np.arange(N),F6, color='green')
pylab.xlabel('Номер строки')
pylab.ylabel('Max')
pylab.title('Третий график')

pylab.subplot(2, 2, 4)
F7 = np.min(f, axis=1)
pylab.bar(np.arange(N), F7, color='orange')
pylab.plot(np.arange(N), F7, color='purple', marker='o', markersize=3)
pylab.xlabel('Номер строки')
pylab.ylabel('Min')
pylab.title('Четвертый график')

plt.show()