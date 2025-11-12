# -*- coding: utf-8 -*-
import tkinter as tk
from collections import deque
import random


W, H = 31, 31
CELL = 22  


BG       = "#000000"
FG_DIM   = "#0c5a2e"   # тусклые точки пола
FG_WALL  = "#22a85a"   # стены
FG_TEXT  = "#39d67b"   # обычные символы
FG_SEEN  = "#66ffb2"   # посещённые
FG_PATH  = "#c8ffdf"   # путь (ярче, но всё ещё зелёный)


CH_WALL  = "█"
CH_FLOOR = "·"         
CH_SEEN  = "•"
CH_PATH  = "▓"
CH_START = "S"
CH_EXIT  = "E"

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабиринт — Terminal Mono")
        wpx, hpx = W*CELL, H*CELL
        self.canvas = tk.Canvas(root, width=wpx, height=hpx, bg=BG, highlightthickness=0)
        self.canvas.pack(padx=6, pady=(6,0))
        self.btn = tk.Button(root, text="Старт", command=self.start, padx=10, pady=6)
        self.btn.pack(pady=(6,8))

       
        self.maze = None
        self.start_xy = None
        self.exit_xy = None

      
        self.queue = None
        self.visited = None
        self.parent = None
        self.found = None
        self.step_after = None
        self.path_after = None

        
        self.cell_id = {}

        self.new_maze()
        self.draw_maze()

    
    def new_maze(self):
        self.maze = [['#'] * W for _ in range(H)]
        sx, sy = W//2, H//2
        self.start_xy = (sx, sy)
        self.maze[sy][sx] = ' '

        def carve(x, y):
            dirs = [(2,0), (-2,0), (0,2), (0,-2)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x+dx, y+dy
                if 0 < nx < W-1 and 0 < ny < H-1 and self.maze[ny][nx] == '#':
                    self.maze[ny - dy//2][nx - dx//2] = ' '
                    self.maze[ny][nx] = ' '
                    carve(nx, ny)
        carve(sx, sy)

        edges = ([(x,0) for x in range(W)]
                 + [(x,H-1) for x in range(W)]
                 + [(0,y) for y in range(H)]
                 + [(W-1,y) for y in range(H)])
        free_edges = [p for p in edges if self.maze[p[1]][p[0]] == ' ']
        if free_edges:
            ex = random.choice(free_edges)
        else:
            side = random.choice(['top','bottom','left','right'])
            if side == 'top': ex = (random.randrange(1,W-1,2), 0)
            elif side == 'bottom': ex = (random.randrange(1,W-1,2), H-1)
            elif side == 'left': ex = (0, random.randrange(1,H-1,2))
            else: ex = (W-1, random.randrange(1,H-1,2))
            self.maze[ex[1]][ex[0]] = ' '
        self.exit_xy = ex
        self.maze[ex[1]][ex[0]] = 'E'

    
    def center(self, x, y):
        return (x*CELL + CELL//2, y*CELL + CELL//2)

    def set_char(self, x, y, ch, fill):
        item = self.cell_id.get((x, y))
        if item is None:
            cx, cy = self.center(x, y)
            item = self.canvas.create_text(
                cx, cy, text=ch, fill=fill,
                font=("Consolas", CELL-6, "bold")
            )
            self.cell_id[(x, y)] = item
        else:
            self.canvas.itemconfigure(item, text=ch, fill=fill)

   
    def draw_maze(self):
        self.canvas.delete("all")
        self.cell_id.clear()
        for y in range(H):
            for x in range(W):
                cell = self.maze[y][x]
                if cell == '#':
                    self.set_char(x, y, CH_WALL, FG_WALL)
                elif cell == 'E':
                    self.set_char(x, y, CH_EXIT, FG_TEXT)
                else:
                    self.set_char(x, y, CH_FLOOR, FG_DIM)
        sx, sy = self.start_xy
        self.set_char(sx, sy, CH_START, FG_TEXT)

    
    def start(self):
        self.btn.config(state="disabled")
        self.cancel_timers()
        self.new_maze()
        self.draw_maze()

        self.queue = deque([self.start_xy])   # O(1)
        self.visited = {self.start_xy}
        self.parent = {}
        self.found = None

        self.step_after = self.root.after(0, self.bfs_step)

    def bfs_step(self):
        if not self.queue or self.found is not None:
            if self.found:
                self.animate_path()
            else:
                self.btn.config(state="normal")
            return

        x, y = self.queue.popleft()
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < W and 0 <= ny < H and self.maze[ny][nx] != '#' and (nx, ny) not in self.visited:
                self.visited.add((nx, ny))
                self.parent[(nx, ny)] = (x, y)
                
                if (nx, ny) != self.start_xy and self.maze[ny][nx] != 'E':
                    self.set_char(nx, ny, CH_SEEN, FG_SEEN)

                if self.maze[ny][nx] == 'E':
                    self.found = (nx, ny)
                    break
                self.queue.append((nx, ny))

        self.step_after = self.root.after(1, self.bfs_step)

    def animate_path(self):
        path = []
        cur = self.found
        while cur != self.start_xy:
            path.append(cur)
            cur = self.parent[cur]
        path.reverse()

        def draw_next(i=0):
            if i >= len(path):
                self.btn.config(state="normal")
                return
            x, y = path[i]
            if (x, y) != self.exit_xy:
                self.set_char(x, y, CH_PATH, FG_PATH)
            self.path_after = self.root.after(10, lambda: draw_next(i+1))

        draw_next()

    def cancel_timers(self):
        if self.step_after:
            try: self.root.after_cancel(self.step_after)
            except: pass
            self.step_after = None
        if self.path_after:
            try: self.root.after_cancel(self.path_after)
            except: pass
            self.path_after = None

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
