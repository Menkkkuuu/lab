import tkinter as tk
from tkinter import messagebox
import random

# ЛОГИКА 
class Ship:
    def __init__(self, cells):
        self.cells = set(cells)
        self.hits = set()
    def is_sunk(self):
        return self.hits == self.cells

class Board:
    def __init__(self):
        self.grid = [[0]*10 for _ in range(10)]
        self.ships = []
        self.shots = set()
    def can_place(self, r, c, size, horiz):
        cells = [(r, c+i) if horiz else (r+i, c) for i in range(size)]
        if any(rr<0 or rr>9 or cc<0 or cc>9 for rr,cc in cells):
            return False
        for rr, cc in cells:
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    nr, nc = rr+dr, cc+dc
                    if 0<=nr<10 and 0<=nc<10 and self.grid[nr][nc]==1:
                        return False
        return True
    def place_ship(self, r, c, size, horiz):
        if not self.can_place(r,c,size,horiz): return False
        cells = [(r,c+i) if horiz else (r+i,c) for i in range(size)]
        self.ships.append(Ship(cells))
        for rr,cc in cells: self.grid[rr][cc]=1
        return True
    def random_placement(self, sizes):
        self.grid=[[0]*10 for _ in range(10)]
        self.ships=[]
        for size in sizes:
            for _ in range(1000):
                r,c=random.randint(0,9),random.randint(0,9)
                if self.place_ship(r,c,size,random.choice([True,False])): break
    def shoot(self,r,c):
        if (r,c) in self.shots: return None
        self.shots.add((r,c))
        if self.grid[r][c]==1:
            self.grid[r][c]=2
            for ship in self.ships:
                if (r,c) in ship.cells:
                    ship.hits.add((r,c))
                    return 'sunk' if ship.is_sunk() else 'hit'
        self.grid[r][c]=3
        return 'miss'
    def all_sunk(self): return all(ship.is_sunk() for ship in self.ships)

class Game:
    def __init__(self):
        self.sizes=[4,3,3,2,2,2,1,1,1,1]
        self.player=Board()
        self.computer=Board()
        self.targets=[(r,c) for r in range(10) for c in range(10)]
        random.shuffle(self.targets)
        self.phase='setup'; self.player_turn=True
        self.setup_idx=0; self.horiz=True
    def place_player_ship(self,r,c):
        if self.setup_idx>=len(self.sizes): return False
        if self.player.place_ship(r,c,self.sizes[self.setup_idx],self.horiz):
            self.setup_idx+=1
            if self.setup_idx>=len(self.sizes): self.start_game()
            return True
        return False
    def random_player_setup(self):
        self.player.random_placement(self.sizes)
        self.setup_idx=len(self.sizes)
        self.start_game()
    def start_game(self):
        self.computer.random_placement(self.sizes)
        self.phase='playing'; self.player_turn=True
    def player_shoot(self,r,c):
        if not self.player_turn or self.phase!='playing': return None
        result=self.computer.shoot(r,c)
        if result and self.computer.all_sunk(): self.phase='ended'; return 'win'
        if result=='miss': self.player_turn=False
        return result
    def computer_shoot(self):
        if self.player_turn or not self.targets: return None,None
        r,c=self.targets.pop()
        result=self.player.shoot(r,c)
        if self.player.all_sunk(): self.phase='ended'; return (r,c),'lose'
        if result=='miss': self.player_turn=True
        return (r,c),result


class GUI:
    def __init__(self, root):
        self.root=root; root.title("Морской бой")
        self.game=Game(); self.cell=40
        self.colors={0:'lightblue',1:'gray',2:'red',3:'blue'}
        self.status=tk.Label(root,text="Расставьте корабли",font=('Arial',14))
        self.status.pack(pady=10)
        bf=tk.Frame(root); bf.pack()
        tk.Button(bf,text="Повернуть",command=self.rotate).pack(side=tk.LEFT,padx=5)
        tk.Button(bf,text="Случайная расстановка",command=self.random_setup).pack(side=tk.LEFT,padx=5)
        tk.Button(bf,text="Новая игра",command=self.new_game).pack(side=tk.LEFT,padx=5)
        mf=tk.Frame(root); mf.pack()
        lf=tk.Frame(mf); lf.pack(side=tk.LEFT,padx=20)
        tk.Label(lf,text="Ваши корабли",font=('Arial',12,'bold')).pack()
        self.pc=tk.Canvas(lf,width=400,height=400); self.pc.pack()
        self.pc.bind('<Button-1>',self.p_click); self.pc.bind('<Motion>',self.p_hover)
        rf=tk.Frame(mf); rf.pack(side=tk.LEFT,padx=20)
        tk.Label(rf,text="Вражеские воды",font=('Arial',12,'bold')).pack()
        self.cc=tk.Canvas(rf,width=400,height=400); self.cc.pack()
        self.cc.bind('<Button-1>',self.c_click)
        self.cc.bind('<Motion>', self.c_hover)  # Наведение на поле врага
        self.hover_rect=None
        self.draw()
    
    def draw(self):
        self.draw_board(self.pc,self.game.player,True)
        self.draw_board(self.cc,self.game.computer,False)
    
    def draw_board(self,canvas,board,show):
        canvas.delete('all')
        for r in range(10):
            for c in range(10):
                x1,y1=c*self.cell,r*self.cell; x2,y2=x1+self.cell,y1+self.cell
                val=board.grid[r][c]
                is_sunk=any(ship.is_sunk() and (r,c) in ship.cells for ship in board.ships)
                color='lightblue' if is_sunk else (self.colors[0] if val==1 and not show else self.colors[val])
                canvas.create_rectangle(x1,y1,x2,y2,fill=color,outline='black')
                if is_sunk:
                    canvas.create_line(x1,y1,x2,y2,fill='red',width=2)
                    canvas.create_line(x1,y2,x2,y1,fill='red',width=2)
    
    #Расстановка 
    def p_click(self,e):
        if self.game.phase!='setup': return
        r,c=e.y//self.cell,e.x//self.cell
        if 0<=r<10 and 0<=c<10 and self.game.place_player_ship(r,c):
            self.draw(); self.update_status()
    
    def p_hover(self,e):
        if self.game.phase!='setup' or self.game.setup_idx>=len(self.game.sizes): return
        r,c=e.y//self.cell,e.x//self.cell; self.draw_board(self.pc,self.game.player,True)
        size=self.game.sizes[self.game.setup_idx]
        if 0<=r<10 and 0<=c<10:
            color='green' if self.game.player.can_place(r,c,size,self.game.horiz) else 'red'
            for rr,cc in [(r,c+i) if self.game.horiz else (r+i,c) for i in range(size)]:
                if 0<=rr<10 and 0<=cc<10:
                    x1,y1=cc*self.cell,rr*self.cell
                    self.pc.create_rectangle(x1,y1,x1+self.cell,y1+self.cell,fill=color,outline='black',stipple='gray50')
    
    #игровой процесс
    def c_click(self,e):
        if self.game.phase!='playing' or not self.game.player_turn: return
        r,c=e.y//self.cell,e.x//self.cell
        if 0<=r<10 and 0<=c<10:
            result=self.game.player_shoot(r,c)
            if result:
                self.draw()
                if result=='win': messagebox.showinfo("Победа","Вы выиграли!"); return
                self.update_status()
                if not self.game.player_turn: self.root.after(500,self.comp_turn)
    
    def c_hover(self,e):
        if self.game.phase!='playing' or not self.game.player_turn: return
        r,c=e.y//self.cell,e.x//self.cell
        self.draw_board(self.cc,self.game.computer,False)
        if 0<=r<10 and 0<=c<10 and (r,c) not in self.game.computer.shots:
            x1,y1=c*self.cell,r*self.cell; x2,y2=x1+self.cell,y1+self.cell
            self.hover_rect=self.cc.create_rectangle(x1,y1,x2,y2,fill='green',outline='black',stipple='gray50')
    
    def comp_turn(self):
        if self.game.phase!='playing' or self.game.player_turn: return
        self.update_status(); pos,result=self.game.computer_shoot()
        if pos:
            self.draw()
            if result=='lose': messagebox.showinfo("Поражение","Компьютер выиграл!"); return
            if not self.game.player_turn: self.root.after(500,self.comp_turn)
            else: self.update_status()
    
    #Кнопки 
    def rotate(self): self.game.horiz=not self.game.horiz
    def random_setup(self): self.game.random_player_setup(); self.draw(); self.update_status()
    def new_game(self): self.game=Game(); self.draw(); self.update_status()
    
    def update_status(self):
        if self.game.phase=='setup' and self.game.setup_idx<len(self.game.sizes):
            size=self.game.sizes[self.game.setup_idx]; left=len(self.game.sizes)-self.game.setup_idx
            self.status.config(text=f"Разместите корабль {size} ({left} осталось)")
        elif self.game.phase=='playing':
            self.status.config(text="Ваш ход" if self.game.player_turn else "Ход компьютера")
        else: self.status.config(text="Игра окончена")


if __name__=="__main__":
    root=tk.Tk(); GUI(root); root.mainloop()
