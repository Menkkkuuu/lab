import tkinter as tk 
import random

grid_w, grid_h = 31, 31
cell = 18
theme = {
    "bg": "#0a0f1f",
    "wall_dark": "#1e2b45",
    "wall_light": "#2f3f63",
    "floor": "#0f1c33",
    "floor_alt": "#132544",
    "start": "#7fffd4",
    "exit": "#ffda7b",
    "visit": "#5ea2ff",
    "path": "#c5e4ff",
    "grid": "#11182b",
}

root = tk.Tk()
root.title("лабиринт")

# центрируем окно по экрану
win_w = grid_w * cell
win_h = grid_h * cell
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x = (screen_w - win_w) // 2
y = (screen_h - win_h) // 2
root.geometry(f"+{x}+{y}")

canvas = tk.Canvas(root, width=win_w, height=win_h, bg=theme["bg"], highlightthickness=0)
canvas.pack()

# матрица лабиринта
maze = [['#'] * grid_w for _ in range(grid_h)]

# генерация лабиринта 
def carve(x, y):
    dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    random.shuffle(dirs)
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 < nx < grid_w - 1 and 0 < ny < grid_h - 1 and maze[ny][nx] == '#':
            maze[ny - dy // 2][nx - dx // 2] = ' '
            maze[ny][nx] = ' '
            carve(nx, ny)

start = (grid_w // 2, grid_h // 2)
maze[start[1]][start[0]] = ' '
carve(*start)

# выход всегда справа
exit_x = grid_w - 1
exit_y = start[1]
for y in range(grid_h):
    if maze[y][exit_x] == ' ':
        exit_y = y
        break
exit_cell = (exit_x, exit_y)
maze[exit_y][exit_x] = 'E'

# тема квадратика 
pat = [
    "..X..",
    ".XXX.",
    "XXXXX",
    ".XXX.",
    "..X..",
]

def draw_tile(px, py, base, accent, outline=False):
    step = cell // 5
    canvas.create_rectangle(
        px, py, px + cell, py + cell,
        fill=theme["bg"],
        outline=theme["grid"] if outline else ""
    )
    for j, line in enumerate(pat):
        for i, ch in enumerate(line):
            color = accent if ch == 'X' else base
            canvas.create_rectangle(
                px + i * step,
                py + j * step,
                px + i * step + step,
                py + j * step + step,
                outline="",
                fill=color
            )

def draw_maze():
    canvas.delete("all")
    for y in range(grid_h):
        for x in range(grid_w):
            code = maze[y][x]
            if code == '#':
                draw_tile(x * cell, y * cell, theme["wall_dark"], theme["wall_light"], outline=True)
            elif code == 'E':
                draw_tile(x * cell, y * cell, theme["floor"], theme["exit"])
            else:
                draw_tile(x * cell, y * cell, theme["floor"], theme["floor_alt"])
    sx, sy = start
    draw_tile(sx * cell, sy * cell, theme["floor"], theme["start"])
    root.update()

draw_maze()


seen = set()
parent = {}
found = None  

def dfs(x, y):
    global found
    if found is not None:  
        return

    seen.add((x, y))

    # подсветка посещенной клетки 
    draw_tile(x * cell, y * cell, theme["floor"], theme["visit"])
    sx, sy = start
    draw_tile(sx * cell, sy * cell, theme["floor"], theme["start"])
    ex, ey = exit_cell
    draw_tile(ex * cell, ey * cell, theme["floor"], theme["exit"])
    root.update()

    # выход - конец 
    if maze[y][x] == 'E':
        found = (x, y)
        show_path()
        return

    # 4 направления 
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if (
            0 <= nx < grid_w
            and 0 <= ny < grid_h
            and maze[ny][nx] != '#'
            and (nx, ny) not in seen
        ):
            parent[(nx, ny)] = (x, y)
            dfs(nx, ny)
            if found is not None:
                return

def show_path():
    cur = found
    path = []
    while cur and cur != start:
        path.append(cur)
        cur = parent.get(cur)
    for x, y in path:
        draw_tile(x * cell, y * cell, theme["floor"], theme["path"])
    sx, sy = start
    draw_tile(sx * cell, sy * cell, theme["floor"], theme["start"])
    ex, ey = exit_cell
    draw_tile(ex * cell, ey * cell, theme["floor"], theme["exit"])
    root.update()


root.after(200, lambda: dfs(*start))
root.mainloop()

