"""
Задание состоит из двух частей.
2 часть – усложнить написанную программу, введя по своему усмотрению в условие минимум одно ограничение
на характеристики объектов (которое будет сокращать количество переборов)  и целевую функцию
для нахождения оптимального  решения.

Вариант 5. В хоккейной команде 18 человек, из них 11 в основном составе (1-вратарь, 4 -  нападающих, 6 – защитников).
Вывести все возможные варианты основных составов команды на игру.
"""

import timeit
import itertools

while True:
    goalies = int(input("Введите количество вратарей (не более 1): "))
    if goalies > 1 or goalies < 1:
        print("Неверное количество вратарей. Введите число не больше 1 и не меньше 1.")
    else:
        break

while True:
    forwards = int(input("Введите количество нападающих (не более 4): "))
    if forwards > 4 or forwards < 1:
        print("Неверное количество нападающих. Введите число не больше 4 и не меньше 1.")
    else:
        break

while True:
    defenders = int(input("Введите количество защитников (не более 6): "))
    if defenders > 6 or defenders < 1:
        print("Неверное количество защитников. Введите число не больше 6 и не меньше 1.")
    else:
        break

# Список всех игроков
all_players = list(range(1, 12))
start_time = timeit.default_timer()

# Функция для генерации вариантов составов
def generate_lineups():
    global defenders, forwards
    goalies_combinations = itertools.combinations(all_players, goalies)
    for goalie in goalies_combinations:
        defenders_combinations = itertools.combinations(all_players, defenders)
        for defender in defenders_combinations:
            forwards_combinations = itertools.combinations(all_players, forwards)
            for forward in forwards_combinations:
                # Проверка на уникальность игроков
                if len(set(goalie).union(set(defender)).union(set(forward))) == 11:
                    # Проверка на ограничение
                    if defenders <= 2:
                        continue
                    # Вывод состава в нужном формате
                    yield list(goalie) + list(defender) + list(forward)

# Целевая функция: Оценивает силу состава по сумме номеров игроков.
def calculate_total_number(lineup):
    return sum(lineup)

# Находим состав с максимальной суммой номеров
best_lineup = max(generate_lineups(), key=calculate_total_number)

print(f"Состав с максимальной суммой номеров: {best_lineup}")

end_time = timeit.default_timer()
print(f"Время выполнения с помощью функций: {end_time - start_time:.2f} секунд")