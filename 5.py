import timeit
from itertools import product

# Названия фруктов
fruits = ['Яблоко', 'Банан', 'Апельсин', 'Груша', 'Киви']
DAYS = 7

# Цена каждого фрукта (в рублях)
fruit_prices = {
    'Яблоко': 12,
    'Банан': 11,
    'Апельсин': 3,
    'Груша': 4,
    'Киви': 14,
    'Виноград': 18,
    'Слива': 6
}

#Ограничение на общую цену меню за 7 дней
MAX_PRICE = 85

#Два метода генерации меню

def algorithmic_menus(fruits, days):
    if days == 1:
        return [(f,) for f in fruits]
    prev = algorithmic_menus(fruits, days - 1)
    return [(f,) + p for f in fruits for p in prev]

def pythonic_menus(fruits, days):
    return list(product(fruits, repeat=days))

# ---------- Сравнение времени ----------
time_alg = timeit.timeit(lambda: algorithmic_menus(fruits, DAYS), number=1)
time_py = timeit.timeit(lambda: pythonic_menus(fruits, DAYS), number=1)

menus_alg = algorithmic_menus(fruits, DAYS)
menus_py = pythonic_menus(fruits, DAYS)

print(f"\n[1] Алгоритмический метод: {len(menus_alg)} вариантов, время: {time_alg:.4f} сек")
print(f"[2] Python itertools.product: {len(menus_py)} вариантов, время: {time_py:.4f} сек")

if time_alg < time_py:
    print("→ Алгоритмический метод быстрее.\n")
else:
    print("→ Python-метод быстрее.\n")

print("--- Примеры первых 10 меню ---")
for i, menu in enumerate(menus_py[:10], 1):
    print(f"{i}) {' | '.join(menu)}")

# ---------- ЧАСТЬ 2: Ограничения и оптимизация ----------

def menu_price(menu):
    return sum(fruit_prices[f] for f in menu)

def is_valid(menu):
    return all(menu.count(fruit) <= 3 for fruit in fruits) and menu_price(menu) <= MAX_PRICE

def count_unique(menu):
    return len(set(menu))

valid_menus = [m for m in menus_py if is_valid(m)]

max_variety = max(count_unique(m) for m in valid_menus)
optimal_menus = [m for m in valid_menus if count_unique(m) == max_variety]

print(f"\nНайдено {len(valid_menus)} допустимых меню (повторы ≤ 3, цена ≤ {MAX_PRICE} руб).")
print(f"Максимальное разнообразие фруктов в меню: {max_variety}")
print(f"Количество оптимальных меню: {len(optimal_menus)}\n")

print("--- Примеры оптимальных меню ---")
for i, menu in enumerate(optimal_menus[:5], 1):
    price = menu_price(menu)
    print(f"{i}) {' | '.join(menu)} — {price} руб.")

# ---------- Финальный шаг: самое дешёвое из самых разнообразных меню ----------

if optimal_menus:
    best_price = min(menu_price(m) for m in optimal_menus)
    best_menu = [m for m in optimal_menus if menu_price(m) == best_price][0]  # Берем первое из лучших
    print("\n=== Самое оптимальное меню (макс. разнообразие + мин. цена) ===")
    print(f"{' | '.join(best_menu)} — {best_price} руб.")
else:
    print("Нет ни одного меню, удовлетворяющего всем условиям.")

