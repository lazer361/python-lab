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

# Генерируем рандомные позицие игроков
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

  # Алгоритмический вариант
  def generate_rosters_iterative(goalies_list, forwards_list, defensemen_list, main_roster_size):
      """Генерирует все возможные основные составы команды итеративно без рекурсии."""
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

      return rosters

  # Вариант с использованием функций Python
  def generate_rosters_functional(goalies_list, forwards_list, defensemen_list, main_roster_size):
    """Генерирует все возможные основные составы команды с использованием функций Python."""
    all_players = goalies_list + forwards_list + defensemen_list
    print(all_players)
    return [
      list(roster)
      for roster in itertools.combinations(all_players, main_roster_size)
    ]

  # Измерение времени выполнения
  rosters_iterative = generate_rosters_iterative(selected_goalie, selected_forwards, selected_defenders, len(final_team))
  iterative_time = timeit.timeit(
      lambda: rosters_iterative,
      number=1
  )
  rosters_functional = generate_rosters_functional(selected_goalie, selected_forwards, selected_defenders, len(final_team))
  functional_time = timeit.timeit(
      lambda: rosters_functional,
      number=1
  )

  # Вывод результатов
  print("Количество возможных составов:", len(rosters_iterative))
  print("Время выполнения итеративного алгоритма:", iterative_time, "секунд")
  print("Время выполнения функционального варианта:", functional_time, "секунд")
  print("\nВсе возможные варианты Алгоритмического варианта:")
  for i, roster in enumerate(rosters_iterative):
      print(f"{i+1}. {roster}")
  print("\nВсе возможные варианты Функционального:")
  for i, roster in enumerate(rosters_functional):
      print(f"{i+1}. {roster}")
else:
  print("Такого состава не существует. Попробуйте ввести так, чтобы основных игроков было 11")