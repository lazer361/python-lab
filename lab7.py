"""
Требуется для своего варианта второй части л.р. №6 (усложненной программы) разработать реализацию с
использованием графического интерфейса. Допускается использовать любую графическую библиотеку питона.
Рекомендуется использовать внутреннюю библиотеку питона  tkinter.

В программе должны быть реализованы минимум одно окно ввода, одно окно вывода (со скролингом), одно текстовое поле,
одна кнопка.
"""

import tkinter as tk
import random
import time
import itertools

def generate_roster():
    output_text.delete("1.0", tk.END)

    num_players = int(num_players_entry.get())
    if num_players != 18:
        output_text.insert(tk.END, "Ошибка: количество игроков должно быть равно 18!\n")
        return

    players = []
    for i in range(num_players):
        position = random.choice(["Вратарь", "Нападающий", "Защитник"])
        player_name = f"{position} {i + 1}"
        players.append(player_name)

    goalies = [p for p in players if "Вратарь" in p]
    forwards = [p for p in players if "Нападающий" in p]
    defenders = [p for p in players if "Защитник" in p]

    selected_goalie = random.sample(goalies, 1)
    if len(forwards) >= 4:
        selected_forwards = random.sample(forwards, 4)
    else:
        output_text.insert(tk.END,f"Недостаточно Нападающих для формирования состава! Количество нападающих: "
                                        f"{len(forwards)}. Нажмите на кнопку: Сгенерировать состав заново.")


    if len(defenders) >= 6:
        selected_defenders = random.sample(defenders, 6)
    else:
        output_text.insert(tk.END, f"Недостаточно защитников для формирования состава! Количество защитников:"
                                         f"{len(defenders)}. Нажмите на кнопку: Сгенерировать состав заново.")
    if len(forwards) >= 4 and len(defenders) >= 6:
        final_team = [selected_goalie] + selected_forwards + selected_defenders

        if len(final_team) == 11:

            # Вывод всех возможных составов
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

            output_text.insert(tk.END, f"\n")
            for roster in rosters_universal:
                output_text.insert(tk.END, f"{roster}\n")
            output_component.insert(tk.END, f"\n {best_roster}\n\n")


        else:
            output_text.insert(tk.END, "Ошибка: не удалось сформировать состав из 11 игроков.\n")


def generate_rosters_universal(goalies_list, forwards_list, defensemen_list, main_roster_size):
    """Генерирует все возможные основные составы команды."""
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

# Создание графического интерфейса
root = tk.Tk()
root.title("Генератор Составов Хоккейной Команды")

num_players_label = tk.Label(root, text="Количество игроков (18):")
num_players_label.grid(row=0, column=0, padx=5, pady=5)

num_players_entry = tk.Entry(root)
num_players_entry.grid(row=0, column=1, padx=5, pady=5)
num_players_entry.insert(0, "18")

generate_button = tk.Button(root, text="Сгенерировать Состав", command=generate_roster)
generate_button.grid(row=1, column=0, columnspan=2, pady=10)

label_title = tk.Label(root, text="Все возможные составы (с ограничением по защитникам):")
label_title.grid(row=2, column=0, pady=5)

output_text = tk.Text(root, wrap=tk.WORD, height=10)
output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

scrollbar = tk.Scrollbar(root, orient= "vertical", command=output_text.yview)
scrollbar.grid(row=3, column=1, sticky="nse")

labelt_average_title = tk.Label(root, text="Состав с максимальной силой:")
labelt_average_title.grid(row=4, column=0, padx=5, pady=5)

output_component = tk.Text(root, wrap=tk.WORD, height=10)
output_component.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

output_text.config(yscrollcommand=scrollbar.set)

root.geometry(f"+{(root.winfo_screenwidth() - 300) // 2}+{(root.winfo_screenheight() - 300) // 2}")
root.mainloop()