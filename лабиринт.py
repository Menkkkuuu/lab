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

# рисуем весь лабиринт
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

visited = set()
path = []
found = False

def dfs(x, y):
    global found
    if found:
        return

    if (x, y) in visited:
        return

    # проверка границ и стен
    if x < 0 or x >= cols or y < 0 or y >= rows:
        return
    if maze[y][x] == 0:
        return

    visited.add((x, y))
    path.append((x, y))

    # рисуем посещение
    draw_cell(x, y, "lightblue")
    root.update()
    root.after(100)

    # нашли выход
    if maze[y][x] == 'E':
        found = True
        # рисуем путь
        for px, py in path:
            draw_cell(px, py, "yellow")
        root.update()
        return

    # идем в 4 стороны
    dfs(x+1, y)
    dfs(x-1, y)
    dfs(x, y+1)
    dfs(x, y-1)

    if not found:
        path.pop()

draw_maze()
root.after(500, lambda: dfs(start[0], start[1]))
root.mainloop()
