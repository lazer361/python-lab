"""
Написать программу, которая читая символы из бесконечной последовательности (эмулируется конечным файлом, читающимся поблочно),
распознает, преобразует и выводит на экран лексемы по определенному правилу.
Лексемы разделены пробелами. Преобразование делать по возможности через словарь.
Для упрощения под выводом числа прописью подразумевается последовательный вывод всех цифр числа.
Регулярные выражения использовать нельзя.

Вариант 5.
Натуральные числа, не превышающие 1 000 000, у которых первые две цифры равны 77.
Выводит на экран числа, без этих 7.
Вычисляется среднее число между минимальным и максимальным и выводится прописью.
"""

# Словарь для преобразования цифр в прописной вид
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
min_number = 0
max_number = 1000000

file = open("input.txt", "r", encoding="utf-8")

while True:
    str_txt = file.readline().split()
    if not str_txt:
        print("\nФайл input.txt в директории проекта закончился")
        break
    else:
        for num in str_txt:
            numbers_str = num.strip().replace(' ', '').replace(',', '')
            for number_str in numbers_str.split():
                # Проверка на число
                if number_str.isdigit():
                    number = int(number_str)
                    if 0 < number <= 1000000 and len(str(number)) >= 3 and str(number)[:2] == '77' and str(number)[:3] != '777':
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