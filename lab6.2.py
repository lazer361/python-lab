"""
Задание состоит из двух частей.
2 часть – усложнить написанную программу, введя по своему усмотрению в условие минимум одно ограничение
на характеристики объектов (которое будет сокращать количество переборов)  и целевую функцию
для нахождения оптимального  решения.

Вариант 5. В хоккейной команде 18 человек, из них 11 в основном составе (1-вратарь, 4 -  нападающих, 6 – защитников).
Вывести все возможные варианты основных составов команды на игру.
"""

import itertools
import time
import random

def get_integer_input(prompt, max_value):
  while True:
    value_input = input(prompt)
    if value_input.isdigit() and 0 <= int(value_input) <= max_value:
      return int(value_input)
    else:
      print(f"Введите целое число от 0 до {max_value}.")

# Получаем ввод пользователя с использованием функции
num_players = int(input("Введите количество игроков (18): "))

# Проверяем, что количество игроков равно 18
if num_players != 18:
    print("Ошибка: количество игроков должно быть равно 18!")
    exit()

# Создаем пустой список игроков
players = []

# Генерируем рандомные имена игроков
for i in range(num_players):
    # Определяем позицию игрока
    position = random.choice(["Вратарь", "Нападающий", "Защитник"])
    # Формируем имя игрока с номером
    player_name = f"{position} {i + 1}"
    # Добавляем игрока в список
    players.append(player_name)

goalies = [p for p in players if "Вратарь" in p]
forwards = [p for p in players if "Нападающий" in p]
defenders = [p for p in players if "Защитник" in p]

# Выбираем случайных игроков по позициям
selected_goalie = random.sample(goalies, 1)
if len(forwards) >= 4:
    selected_forwards = random.sample(forwards, 4)
else:
    print(f"Недостаточно Нападающих для формирования состава! Количество нападающих: {len(forwards)}. Запустите программу ещё раз.")
    exit()

if len(defenders) >= 6:
    selected_defenders = random.sample(defenders, 6)
else:
    print(f"Недостаточно защитников для формирования состава! Количество защитников:{len(defenders)}. Запустите программу ещё раз.")
    exit()

# Формируем окончательный состав
final_team = [selected_goalie] + selected_forwards + selected_defenders

if len(final_team) == 11:
  def generate_rosters_universal(goalies_list, forwards_list, defensemen_list, main_roster_size):
    """Генерирует все возможные основные составы команды с использованием функций Python."""
    rosters = []
    all_players = goalies_list + forwards_list + defensemen_list

    if len(all_players) < main_roster_size:
        print(f"Ошибка: Недостаточно игроков для формирования состава из {main_roster_size} человек.")
        return rosters

    # Генерируем перестановки без рекурсии
    for i in range(len(all_players)):
        for j in range(i + 1, len(all_players)):
            all_players[i], all_players[j] = all_players[j], all_players[i]
            rosters.append(all_players[:main_roster_size].copy())
            all_players[i], all_players[j] = all_players[j], all_players[i]

    # Ограничение: генерируем только составы, где не больше 2 защитников на льду одновременно
    valid_rosters = []
    for roster in rosters:
      if roster.count('Защитник') <= 2:
        valid_rosters.append(roster)
    return valid_rosters

  def calculate_team_strength(roster):
    """Целевая функция:  Оценивает силу состава по среднему номеру игрока."""
    total_number = 0
    for player in roster:
      number = int(player.split()[-1])
      total_number += number
    return total_number / len(roster)

  # Измерение времени выполнения

  start_time = time.time()
  rosters_universal = generate_rosters_universal(selected_goalie, selected_forwards, selected_defenders, len(final_team))
  end_time = time.time()
  universal_time = end_time - start_time

  # Находим состав с максимальной силой
  best_roster = None
  max_strength = float('-inf')
  for roster in rosters_universal:
    strength = calculate_team_strength(roster)
    if strength > max_strength:
      max_strength = strength
      best_roster = roster

  # Вывод результатов
  print("Время выполнения универсального варианта:", universal_time, "секунд")
  print("\nВсе возможные варианты Функционального:")
  for i, roster in enumerate(rosters_universal):
      print(f"{i+1}. {roster}")

  print(f"\nСостав с максимальной силой: {best_roster}")
  print(f"Сила состава: {max_strength}")
else:
  print("Такого состава не существует. Попробуйте ввести так, чтобы основных игроков было 11")