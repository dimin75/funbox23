# Пример программы в стиле функционального программирования на Python

# Импорт функций из модуля functools
from functools import reduce

# Функция вычисления факториала с использованием рекурсии
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

# Функция для проверки четности числа
def is_even(num):
    return num % 2 == 0

# Функция для возведения числа в квадрат
def square(num):
    return num * num

# Функция для сложения двух чисел
def add(a, b):
    return a + b

# Функция для перемножения двух чисел
def multiply(a, b):
    return a * b

# Основная функция
def main():
    # Вычисление факториала числа 5
    print("Факториал числа 5:", factorial(5))

    # Фильтрация списка чисел и оставление только четных чисел
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_numbers = list(filter(is_even, numbers))
    print("Четные числа:", even_numbers)

    # Возведение в квадрат всех чисел из списка
    squared_numbers = list(map(square, numbers))
    print("Квадраты чисел:", squared_numbers)

    # Вычисление суммы всех чисел из списка
    sum = reduce(add, numbers)
    print("Сумма чисел:", sum)

    # Вычисление произведения всех чисел из списка
    product = reduce(multiply, numbers)
    print("Произведение чисел:", product)

# Вызов основной функции
if __name__ == "__main__":
    main()
