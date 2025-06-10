import timeit
import matplotlib.pyplot as plt
import math

# Рекурсия
def F_rec(n):
    if n == 1:
        return 1
    sign = -1 if n % 2 == 1 else 1
    return sign * (2 * F_rec(n - 1) - G_rec(n - 1))

def G_rec(n: int):
    if n == 1:
        return 1
    return G_rec(n - 1) + 2 * F_rec(n - 1) / math.factorial(2 * n)

# Итерация 
def F_G_iter(n):
    F_pr, G_pr = 1, 1
    fact = 2  # (2*1)! = 2
    for i in range(2, n + 1):
        # Факториал: (2i)! = (2i - 1)! * (2i - 1) * (2i)
        fact *= (2 * i - 1) * (2 * i)
        sign = -1 if i % 2 == 1 else 1
        F_curr = sign * (2 * F_pr - G_pr)
        G_curr = G_pr + 2 * F_pr / fact
        F_pr, G_pr = F_curr, G_curr
    return F_pr, G_pr

# Сравнение времени выполнения
if __name__ == "__main__":
    results = []
    for i in range(2, 20):
        try:
            t_rec = timeit.timeit(lambda: F_rec(i), number=1)
        except RecursionError:
            t_rec = None
        t_itr = timeit.timeit(lambda: F_G_iter(i), number=1)
        results.append((i, t_rec, t_itr))

    # Вывод таблицы
    print("n | Recursive Time (s) | Iterative Time (s)")
    print("-" * 40)
    for r in results:
        n, t_rec, t_itr = r
        if t_rec is None:
            t_rec_str = "N/A"
        else:
            t_rec_str = f"{t_rec:.6f}"
        t_itr_str = f"{t_itr:.6f}"
        print(f"{n:2d} | {t_rec_str:>15} | {t_itr_str:>15}")

    # График
    plt.figure(figsize=(10, 6))
    # Для рекурсии: только те n, где t_rec не None
    plt.plot([r[0] for r in results if r[1] is not None], 
             [r[1] for r in results if r[1] is not None], 
             label="Рекурсия", marker='o')
    # Для итерации: все n
    plt.plot([r[0] for r in results], 
             [r[2] for r in results], 
             label="Итерация", marker='s')
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение времени выполнения: рекурсивный vs итеративный подход")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
