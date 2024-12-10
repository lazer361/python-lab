'''
Задана рекуррентная функция. Область определения функции – натуральные числа.
Написать программу сравнительного вычисления данной функции рекурсивно и итерационно (значение, время).
Определить (смоделировать) границы применимости рекурсивного и итерационного подхода.
Результаты сравнительного исследования времени вычисления представить в табличной и графической форме в виде отчета по лабораторной работе.
5.	F(1) = 1; G(1) = 1; F(n) = (-1)n*(F(n–1) – 2*G(n–1)), G(n) = F(n–1) /(2n)! + 2*G(n–1), при n >=2
'''

import timeit
import matplotlib.pyplot as plt


# Функция для вычисления факториала числа
last_factorial = 1
def dynamic_factorial(n):
    global last_factorial
    last_factorial *= (2*n*(2*n-1))
    return last_factorial

# Рекурсивная функция для вычисления факториала
def recursive_factorial(n):
    if n == 1:
        return 1
    else:
        return n * recursive_factorial(n-1)

# Итеративная функция для вычисления факториала
result = 1
k = 2
def iterative_factorial(n):
    global result, k
    for i in range(k, n+1):
        result *= i
        k = i
    return result

last_G_value = 1
last_F_value = 1

# Функция для вычисления значения G
def dynamic_G(n):
    global last_G_value, last_F_value
    if n == 1:
        last_G_value = 1
        return last_G_value
    else:
        last_G_value = dynamic_F(n - 1) / (dynamic_factorial(2 * n) + 2* dynamic_G(n - 1))
        return last_G_value

# Функция для вычисления значения F
step = -1
def dynamic_F(n):
    global last_G_value, last_F_value, step
    if n == 1:
        last_F_value = 1
        return last_F_value
    else:
        step *= -1
        last_F_value = step * (dynamic_F(n - 1) - 2 * dynamic_G(n - 1))
        return last_F_value

# Функция для записи времени
def score_time(func, n):
    return timeit.timeit(lambda: func(n), number=1000)

# Значения n для которых мы хотим измерить время выполнения
n_values = range(2, 11)
recursive_times = []
iterative_times = []


# Измерение времени выполнения для каждого значения n
for n in n_values:
    recursive_times.append(score_time(recursive_factorial, n))
    iterative_times.append(score_time(iterative_factorial, n))


# Вывод результатов в табличной форме
print(f"{'n':<10}{'Рекурсивное время (мс)':<25}{'Итерационное время (мс)':<25}")
for i, n in enumerate(n_values):
    print(f"{n:<10}{recursive_times[i]:<25}{iterative_times[i]:<25}")

print(dynamic_G(5))
print(dynamic_F(5))

# Построение и вывод графика результатов
plt.plot(n_values, recursive_times, label='Рекурсивно')
plt.plot(n_values, iterative_times, label='Итерационно')
plt.xlabel('n')
plt.ylabel('Время (в миллисекундах)')
plt.legend()
plt.title('Сравнение времени вычисления функции F(n)')
plt.show()
