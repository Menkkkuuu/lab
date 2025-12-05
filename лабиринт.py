import tkinter as tk

# лабиринт: 0=стена, 1=путь, S=старт, E=выход
maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 'S', 1, 1, 0, 1, 1, 1, 0, 'E', 0],
    [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 'E', 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

cell = 40
rows = len(maze)
cols = len(maze[0])

root = tk.Tk()
root.title("DFS лабиринт")
canvas = tk.Canvas(root, width=cols*cell, height=rows*cell)
canvas.pack()

# найти старт
start = None
for y in range(rows):
    for x in range(cols):
        if maze[y][x] == 'S':
            start = (x, y)

# рисуем клетку
def draw_cell(x, y, color):
    canvas.create_rectangle(x*cell, y*cell, x*cell+cell, y*cell+cell, fill=color, outline="gray")

# рисуем лабиринт
def draw_maze():
    for y in range(rows):
        for x in range(cols):
            c = maze[y][x]
            if c == 0:
                draw_cell(x, y, "black")
            elif c == 'S':
                draw_cell(x, y, "green")
            elif c == 'E':
                draw_cell(x, y, "red")
            else:
                draw_cell(x, y, "white")

all_paths = []  # все пути к выходам

def dfs(x, y, visited, path):
    # проверка границ и стен
    if x < 0 or x >= cols or y < 0 or y >= rows:
        return
    if maze[y][x] == 0 or (x, y) in visited:
        return

    visited.add((x, y))
    path.append((x, y))

    # нашли выход - сохраняем путь
    if maze[y][x] == 'E':
        all_paths.append(path.copy())
    else:
        # идем в 4 стороны
        dfs(x+1, y, visited, path)
        dfs(x-1, y, visited, path)
        dfs(x, y+1, visited, path)
        dfs(x, y-1, visited, path)

    path.pop()
    visited.remove((x, y))

def show_paths():
    colors = ["yellow", "orange", "cyan", "pink", "lime"]
    for i, p in enumerate(all_paths):
        for x, y in p:
            draw_cell(x, y, colors[i % len(colors)])
    # перерисуем старт и выходы
    for y in range(rows):
        for x in range(cols):
            if maze[y][x] == 'S':
                draw_cell(x, y, "green")
            elif maze[y][x] == 'E':
                draw_cell(x, y, "red")

draw_maze()
dfs(start[0], start[1], set(), [])
root.after(500, show_paths)
root.mainloop()
