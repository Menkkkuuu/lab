import time
import matplotlib.pyplot as plt

# Функция для вычисления факториала с мемоизацией ( для рекурсии ) 
def factorial(k, memo={}):
    if k in memo:
        return memo[k]
    if k == 0 or k == 1:
        memo[k] = 1
        return 1
    memo[k] = k * factorial(k - 1, memo)
    return memo[k]

# Рекурсивные функции с мемоизацией
def F_recursive(n, memo_F, memo_G):
    if n in memo_F:
        return memo_F[n]
    if n == 1:
        memo_F[1] = 1
        return 1
    sign = (-1) ** n
    memo_F[n] = sign * (F_recursive(n - 1, memo_F, memo_G) - 2 * G_recursive(n - 1, memo_F, memo_G))
    return memo_F[n]

def G_recursive(n, memo_F, memo_G):
    if n in memo_G:
        return memo_G[n]
    if n == 1:
        memo_G[1] = 1
        return 1
    memo_G[n] = F_recursive(n - 1, memo_F, memo_G) / factorial(2 * n) + 2 * G_recursive(n - 1, memo_F, memo_G)
    return memo_G[n]

# Итеративная функция 
def F_iterative(n):
    if n == 1:
        return 1
    F = [0] * (n + 1)
    G = [0.0] * (n + 1)
    F[1] = 1
    G[1] = 1.0
    for i in range(2, n + 1):
        sign = (-1) ** i
        F[i] = sign * (F[i - 1] - 2 * G[i - 1])
        fact_2i = factorial(2 * i)
        G[i] = F[i - 1] / fact_2i + 2 * G[i - 1]
    return F[n]

# Функция для измерения времени
def measure_time(func, n, *args):
    start = time.perf_counter()
    result = func(n, *args)
    end = time.perf_counter()
    return result, end - start

# Основная программа
n_values = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30]
recursive_times = []
iterative_times = []
recursive_values = []
iterative_values = []

print("n\tРекурсия\t\tВремя (рек)\tИтерация\t\tВремя (итер)")
print("-" * 80)
for n in n_values:
    # Создаем новые словари для мемоизации для каждого n
    memo_F = {}
    memo_G = {}
    res_rec, time_rec = measure_time(F_recursive, n, memo_F, memo_G)
    res_iter, time_iter = measure_time(F_iterative, n)
    
    recursive_times.append(time_rec)
    iterative_times.append(time_iter)
    recursive_values.append(res_rec)
    iterative_values.append(res_iter)
    
    print(f"{n}\t{res_rec:.6f}\t\t{time_rec:.6f}\t{res_iter:.6f}\t\t{time_iter:.6f}")

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(n_values, recursive_times, label="Рекурсия (с мемоизацией)", marker='o')
plt.plot(n_values, iterative_times, label="Итерация", marker='s')
plt.xlabel("n")
plt.ylabel("Время выполнения (сек)")
plt.title("Сравнение времени выполнения рекурсивного и итеративного подходов")
plt.legend()
plt.grid(True)
plt.savefig("time_comparison.png")
plt.show()
