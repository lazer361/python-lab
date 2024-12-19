import pandas as pd
import matplotlib.pyplot as plt

# Пример данных: список маршрутов с выручкой и водителями
data = {
    'Маршрут': ['Маршрут 1', 'Маршрут 2', 'Маршрут 3', 'Маршрут 4'],
    'Водитель': ['Иван', 'Петр', 'Мария', 'Иван'],
    'Выручка': [15000, 23000, 18000, 27000]
}

# Создаем DataFrame
df = pd.DataFrame(data)

# Функция для визуализации обеих диаграмм в одном окне
def plot_combined_charts(df):
    # Группировка данных для диаграмм
    revenue_by_route = df.groupby('Маршрут')['Выручка'].sum()
    revenue_by_driver = df.groupby('Водитель')['Выручка'].sum()

    # Создаем один график с двумя подграфиками
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Круговая диаграмма
    axes[0].pie(revenue_by_route, labels=revenue_by_route.index, autopct='%1.1f%%', startangle=140)
    axes[0].set_title("Распределение выручки по маршрутам")

    # Столбиковая диаграмма
    axes[1].bar(revenue_by_driver.index, revenue_by_driver)
    axes[1].set_title("Выручка по водителям")
    axes[1].set_ylabel("Выручка")
    axes[1].set_xlabel("Водитель")

    # Общий заголовок и отображение
    plt.suptitle("Анализ выручки")
    plt.tight_layout()
    plt.show()

# Вызов функции для построения диаграмм
plot_combined_charts(df)
