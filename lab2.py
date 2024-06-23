"""
Написать программу, решающую задачу из 1 лабораторной работы (в соответствии со своим вариантом) со следующими изменениями:
1.	Входной файл является обыкновенным (т.е. нет требования на «бесконечность» файла);
2.	Распознавание и обработку делать  через регулярные выражения;
3.	В вариантах, где есть параметр (например К), допускается его заменить на любое число;
4.	Все остальные требования соответствуют варианту задания лабораторной работы №1.

Вариант 5.
Натуральные числа, не превышающие 1 000 000, у которых первые две цифры равны 77.
Выводит на экран числа, без этих 7.
Вычисляется среднее число между минимальным и максимальным и выводится прописью.
"""
import re

numbers_dict = {
    '0': 'ноль',
    '1': 'один',
    '2': 'два',
    '3': 'три',
    '4': 'четыре',
    '5': 'пять',
    '6': 'шесть',
    '7': 'семь',
    '8': 'восемь',
    '9': 'девять'
}

filtered_numbers = []
min_number = float('inf')
max_number = float('-inf')

with open("input.txt", "r", encoding="utf-8") as file:
    content = file.read()

    # Регулярное выражение для поиска чисел, удовлетворяющих условию
    pattern = r"\b77(?!7)\d{1,9}\b"
    matches = re.findall(pattern, content)

    for match in matches:
        number = int(match)
        filtered_numbers.append(number)
        min_number = min(min_number, number)
        max_number = max(max_number, number)

if not filtered_numbers:
    print("Нет чисел, удовлетворяющих условию")
else:
    print("Числа без цифры '7':")
    for num in filtered_numbers:
        print(str(num).replace('7', ''), end=' ')

    avg = (min_number + max_number) / 2
    print("\nCреднее число между минимальным и максимальным в прописном виде:")

    avg_str = str(int(avg))
    result = ''
    for digit in avg_str:
        if digit in numbers_dict:
            result += numbers_dict[digit] + ' '

    print(result.strip())