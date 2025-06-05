import timeit
import matplotlib.pyplot as plt
import math

# Рекурсивная реализация
def F_rec(n):
    if n == 1:
        return 1
    sign = -1 if n % 2 == 1 else 1
    return sign * (2 * F_rec(n - 1) - G_rec(n - 1))

def G_rec(n):
    if n == 1:
        return 1
    return 2 * F_rec(n - 1) / math.factorial(2 * n) + G_rec(n - 1)

# Итерационная реализация
def F_G_iter(n):
    F = [0] * (n + 1)
    G = [0] * (n + 1)
    F[1] = G[1] = 1

    factorial = math.factorial(2)  # (2 * 1)! = 2

    for i in range(2, n + 1):
        sign = -1 if i % 2 == 1 else 1
        F[i] = sign * (2 * F[i - 1] - G[i - 1])
        factorial *= (2 * i - 1) * (2 * i)  # (2n)! = (2n - 1)*(2n)
        G[i] = 2 * F[i - 1] / factorial + G[i - 1]

    return F[n], G[n]

# Сравнение времени выполнения
results = []
for i in range(2, 20):
    try:
        t_rec = timeit.timeit(lambda: F_rec(i), number=1)
    except RecursionError:
        t_rec = None
    t_itr = timeit.timeit(lambda: F_G_iter(i), number=1)
    results.append((i, t_rec, t_itr))

# Функция для вывода таблицы
def print_results(results):
    # Заголовок таблицы
    print(f"{'n':<5} {'Recursive Time (s)':<20} {'Iterative Time (s)':<20}")
    print("-" * 45)  # Разделительная линия
    # Вывод строк таблицы
    for row in results:
        n, t_rec, t_itr = row
        t_rec_str = "RecursionError" if t_rec is None else f"{t_rec:.6f}"
        print(f"{n:<5} {t_rec_str:<20} {t_itr:.6f}")

# Вывод таблицы
print_results(results)

# График
plt.figure(figsize=(10, 6))
plt.plot([row[0] for row in results], [row[1] for row in results], label="Рекурсия", marker='o', color='blue')
plt.plot([row[0] for row in results], [row[2] for row in results], label="Итерация", marker='s', color='green')
plt.xlabel("n")
plt.ylabel("Время (сек)")
plt.title("Сравнение времени выполнения: рекурсивный vs итеративный подход")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
import timeit
import matplotlib.pyplot as plt
import math

# Рекурсивная реализация
def F_rec(n):
    if n == 1:
        return 1
    sign = -1 if n % 2 == 1 else 1
    return sign * (2 * F_rec(n - 1) - G_rec(n - 1))

def G_rec(n):
    if n == 1:
        return 1
    return 2 * F_rec(n - 1) / math.factorial(2 * n) + G_rec(n - 1)

# Итерационная реализация
def F_G_iter(n):
    F = [0] * (n + 1)
    G = [0] * (n + 1)
    F[1] = G[1] = 1

    factorial = math.factorial(2)  # (2 * 1)! = 2

    for i in range(2, n + 1):
        sign = -1 if i % 2 == 1 else 1
        F[i] = sign * (2 * F[i - 1] - G[i - 1])
        factorial *= (2 * i - 1) * (2 * i)  # (2n)! = (2n - 1)*(2n)
        G[i] = 2 * F[i - 1] / factorial + G[i - 1]

    return F[n], G[n]

# Сравнение времени выполнения
results = []
for i in range(2, 20):
    try:
        t_rec = timeit.timeit(lambda: F_rec(i), number=1)
    except RecursionError:
        t_rec = None
    t_itr = timeit.timeit(lambda: F_G_iter(i), number=1)
    results.append((i, t_rec, t_itr))

# Функция для вывода таблицы
def print_results(results):
    # Заголовок таблицы
    print(f"{'n':<5} {'Recursive Time (s)':<20} {'Iterative Time (s)':<20}")
    print("-" * 45)  # Разделительная линия
    # Вывод строк таблицы
    for row in results:
        n, t_rec, t_itr = row
        t_rec_str = "RecursionError" if t_rec is None else f"{t_rec:.6f}"
        print(f"{n:<5} {t_rec_str:<20} {t_itr:.6f}")

# Вывод таблицы
print_results(results)

# График
plt.figure(figsize=(10, 6))
plt.plot([row[0] for row in results], [row[1] for row in results], label="Рекурсия", marker='o', color='blue')
plt.plot([row[0] for row in results], [row[2] for row in results], label="Итерация", marker='s', color='green')
plt.xlabel("n")
plt.ylabel("Время (сек)")
plt.title("Сравнение времени выполнения: рекурсивный vs итеративный подход")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
