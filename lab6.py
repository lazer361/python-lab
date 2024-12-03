"""
Задание состоит из двух частей.
1 часть – написать программу в соответствии со своим вариантом задания. Написать 2 варианта формирования
(алгоритмический и с помощью функций Питона), сравнив по времени их выполнение.

Вариант 5. В хоккейной команде 18 человек, из них 11 в основном составе (1-вратарь, 4 -  нападающих, 6 – защитников).
Вывести все возможные варианты основных составов команды на игру.
"""

"""1 Часть"""
import itertools
import timeit

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

# Список всех игроков (представим, что игроки пронумерованы)
all_players = list(range(1, 12))

lineups = []
start_time = timeit.default_timer()

# Перебор вариантов составов
for goalie in range(1, 2):
    for forward1 in range(2, 7):
        for forward2 in range(7, 12):
            for forward3 in range(12, 17):
                for forward4 in range(17, 19):
                    for defender1 in range(2, 7):
                        for defender2 in range(7, 12):
                            for defender3 in range(12, 17):
                                for defender4 in range(17, 19):
                                    for defender5 in range(2, 7):
                                        for defender6 in range(7, 12):
                                            # Проверка на уникальность игроков
                                            if len(set([goalie, defender1, defender2, defender3, defender4, defender5, defender6, forward1, forward2, forward3, forward4])) == 11:
                                                # Вывод состава в нужном формате
                                                print(f"Вратарь {goalie}, Защитник {defender1}, Защитник {defender2}, Защитник {defender3}, Защитник {defender4}, Защитник {defender5}, Защитник {defender6}, Нападающий {forward1}, Нападающий {forward2}, Нападающий {forward3}, Нападающий {forward4}")

end_time = timeit.default_timer()
print(f"Время выполнения алгоритма: {end_time - start_time:.2f} секунд")

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
                    yield list(goalie) + list(defender) + list(forward)

# Вывод всех вариантов составов
for lineup in generate_lineups():
    print(f"Вратарь {lineup[0]}, Защитник {lineup[1]}, Защитник {lineup[2]}, Защитник {lineup[3]}, Защитник {lineup[4]}, Защитник {lineup[5]}, Защитник {lineup[6]}, Нападающий {lineup[7]}, Нападающий {lineup[8]}, Нападающий {lineup[9]}, Нападающий {lineup[10]}")

end_time = timeit.default_timer()
print(f"Время выполнения с помощью функций: {end_time - start_time:.2f} секунд")
