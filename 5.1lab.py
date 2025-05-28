from itertools import combinations
import timeit


players = {
    'Вратарь': ['Г1', 'Г2', 'Г3'],                 
    'Нападающий': ['Н1', 'Н2', 'Н3', 'Н4', 'Н5', 'Н6'], 
    'Защитник': ['З1', 'З2', 'З3', 'З4', 'З5', 'З6', 'З7', 'З8', 'З9']  
}


required = {'Вратарь': 1, 'Нападающий': 4, 'Защитник': 6}


def algorithmic_method(players, required):
    from itertools import product

    gk_combos = list(combinations(players['Вратарь'], required['Вратарь']))
    fwd_combos = list(combinations(players['Нападающий'], required['Нападающий']))
    def_combos = list(combinations(players['Защитник'], required['Защитник']))

    result = [g + f + d for g in gk_combos for f in fwd_combos for d in def_combos]
    return result


def python_method(players, required):
    gk_combos = list(combinations(players['Вратарь'], required['Вратарь']))
    fwd_combos = list(combinations(players['Нападающий'], required['Нападающий']))
    def_combos = list(combinations(players['Защитник'], required['Защитник']))
    return [g + f + d for g in gk_combos for f in fwd_combos for d in def_combos]


time_algo = timeit.timeit(lambda: algorithmic_method(players, required), number=1)
time_py = timeit.timeit(lambda: python_method(players, required), number=1)

algo_combinations = algorithmic_method(players, required)
py_combinations = python_method(players, required)

print(f"Алгоритмический метод: {len(algo_combinations)} комбинаций, {time_algo:.6f} секунд")
print(f"Python метод: {len(py_combinations)} комбинаций, {time_py:.6f} секунд")

print("\n--- Примеры составов ---")
for i, lineup in enumerate(py_combinations[:10], 1):  
    print(f"{i}) {' | '.join(lineup)}")

player_prices = {name: i * 10 + 50 for i, role in enumerate(players.values()) for name in role}
max_price = 1000

def optimized_method(players, required, prices, max_price):
    all_combos = python_method(players, required)
    return [
        c for c in all_combos
        if sum(prices[p] for p in c) <= max_price
    ]

optimal_combinations = optimized_method(players, required, player_prices, max_price)

print(f"\nОптимизированных составов (стоимость ≤ {max_price}): {len(optimal_combinations)}")
for i, lineup in enumerate(optimal_combinations[:10], 1):  # ограничим вывод
    price = sum(player_prices[p] for p in lineup)
    print(f"{i}) {' | '.join(lineup)} — {price} очков")
