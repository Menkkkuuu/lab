import time
from itertools import permutations

# Список всех фруктов (7 штук)
fruits = ["яблоко", "банан", "груша", "апельсин", "киви", "манго", "персик"]
# Ограничение: используем только 4 фрукта
selected_fruits = fruits[:4]  # Берём первые 4: яблоко, банан, груша, апельсин

# Целевая функция: считаем количество яблок в меню
def count_apples(menu):
    return menu.count("яблоко")  # Возвращает, сколько раз яблоко в меню

# Вариант 1: Алгоритмический (простой цикл)
def simple_loop():
    print("Вариант 1: Алгоритмический (цикл)")
    menu = []
    # Для 7 дней выбираем фрукты по очереди, повторяя
    for i in range(7):
        fruit = selected_fruits[i % 4]  # Циклически берём из 4 фруктов
        menu.append(fruit)
        print(f"День {i+1}: {fruit}")
    apple_count = count_apples(menu)
    print(f"Количество яблок: {apple_count}")
    print()
    return apple_count

# Вариант 2: С использованием permutations
def using_permutations():
    print("Вариант 2: С использованием permutations")
    best_menu = None
    min_apples = float('inf')  # Начинаем с бесконечности, чтобы найти минимум
    # Генерируем перестановки из 4 фруктов для 4 дней
    perms = list(permutations(selected_fruits, 4))
    # Проверяем только первые 10 комбинаций для скорости
    for perm in perms[:10]:
        # Создаём меню на 7 дней, повторяя фрукты
        menu = list(perm) + [perm[i % 4] for i in range(3)]  # Дополняем до 7 дней
        apple_count = count_apples(menu)
        if apple_count < min_apples:
            min_apples = apple_count
            best_menu = menu
        print(f"Вариант меню: {menu}, Яблок: {apple_count}")
    print(f"\nЛучшее меню: {best_menu}")
    print(f"Минимальное количество яблок: {min_apples}")
    print()
    return min_apples

# Измеряем время выполнения для Варианта 1
start_time = time.time()
apples_loop = simple_loop()
end_time = time.time()
time_loop = end_time - start_time
print(f"Время выполнения Варианта 1: {time_loop:.6f} секунд")

# Измеряем время выполнения для Варианта 2
start_time = time.time()
apples_perms = using_permutations()
end_time = time.time()
time_perms = end_time - start_time
print(f"Время выполнения Варианта 2: {time_perms:.6f} секунд")

# Сравнение времени
if time_loop < time_perms:
    print("Вариант 1 (цикл) быстрее!")
else:
    print("Вариант 2 (permutations) быстрее!")

# Сравнение по количеству яблок
if apples_loop < apples_perms:
    print("Вариант 1 даёт меньше яблок!")
elif apples_perms < apples_loop:
    print("Вариант 2 даёт меньше яблок!")
else:
    print("Оба варианта дают одинаковое количество яблок!")
