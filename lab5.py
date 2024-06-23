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
last_factorial_value = 1
def dynamic_factorial(n):
    global last_factorial_value
    last_factorial_value = n * last_factorial_value
    return last_factorial_value

# Рекурсивная функция для вычисления факториала
def recursive_factorial(n):
    if n == 1:
        return 1
    else:
        return n * recursive_factorial(n-1)

# Итеративная функция для вычисления факториала
def iterative_factorial(n):
    result = 1
    for i in range(2, n+1):
        result *= i
    return result

last_g_value = 1
last_f_value = 1

# Функция для вычисления значения G
def calculate_g(n):
    global last_g_value, last_f_value
    if n == 1:
        return 1
    else:
        last_g_value = calculate_f(n-1) / (dynamic_factorial(2 * n) + (2 * calculate_g(n-1)))
        return last_g_value

# Функция для вычисления значения F
step = 1
def calculate_f(n):
    global last_g_value, last_f_value
    if n == 1:
        return 1
    else:
        global step
        step *= -1
        last_f_value = step * ((calculate_f(n-1) - 2 * calculate_g(n-1)))
        return last_f_value

# Функция для записи времени
def measure_time(func, n):
    return timeit.timeit(lambda: func(n), number=1000)

# Значения n для которых мы хотим измерить время выполнения
n_values = range(2, 11)
recursive_times = []
iterative_times = []

# Измерение времени выполнения для каждого значения n
for n in n_values:
    recursive_times.append(measure_time(recursive_factorial, n))
    iterative_times.append(measure_time(iterative_factorial, n))

# Вывод результатов в табличной форме
print(f"{'n':<10}{'Рекурсивное время (мс)':<25}{'Итерационное время (мс)':<25}")
for i, n in enumerate(n_values):
    print(f"{n:<10}{recursive_times[i]:<25}{iterative_times[i]:<25}")

# Построение и вывод графика результатов
plt.plot(n_values, recursive_times, label='Рекурсивно')
plt.plot(n_values, iterative_times, label='Итерационно')
plt.xlabel('n')
plt.ylabel('Время (в миллисекундах)')
plt.legend()
plt.title('Сравнение времени вычисления функции F(n)')
plt.show()