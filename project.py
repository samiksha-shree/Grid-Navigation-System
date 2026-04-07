import tkinter as tk
import heapq

CELL = 30
ROWS, COLS = 15, 20
W, H = COLS*CELL, ROWS*CELL

START = (ROWS//2, 0)
END   = (ROWS//2, COLS-1)

# ───────── A* ─────────
class AStar:
    def __init__(self, grid):
        self.grid = grid

    def h(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def find_path(self, start, end):
        pq = [(0, start)]
        came = {}
        cost = {start: 0}

        while pq:
            _, cur = heapq.heappop(pq)

            if cur == end:
                path = []
                while cur != start:
                    path.append(cur)
                    cur = came[cur]
                return path[::-1]

            r, c = cur
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if 0<=nr<ROWS and 0<=nc<COLS and self.grid[nr][nc]==0:
                    new_cost = cost[cur] + 1
                    if (nr,nc) not in cost or new_cost < cost[(nr,nc)]:
                        cost[(nr,nc)] = new_cost
                        heapq.heappush(pq, (new_cost + self.h((nr,nc), end), (nr,nc)))
                        came[(nr,nc)] = cur
        return []

# ───────── Enemy ─────────
class Enemy:
    def __init__(self, start):
        self.pos = list(start)
        self.path = []

    def update(self):
        if self.path:
            self.pos = list(self.path.pop(0))

# ───────── Game ─────────
class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=W, height=H, bg="black")
        self.canvas.pack()

        self.grid = [[0]*COLS for _ in range(ROWS)]
        self.astar = AStar(self.grid)

        self.enemy = Enemy(START)
        self.enemy.path = self.astar.find_path(START, END)

        self.game_over = False

        self.canvas.bind("<Button-1>", self.click)
        self.loop()

    def click(self, e):
        if self.game_over:
            return

        r, c = e.y//CELL, e.x//CELL
        if (r,c)==START or (r,c)==END:
            return

        self.grid[r][c] = 1 - self.grid[r][c]

        path = self.astar.find_path(START, END)
        if not path:
            self.grid[r][c] = 0
        else:
            self.enemy.path = path

    def check_collision(self):
        if tuple(self.enemy.pos) == END:
            self.game_over = True

    def draw(self):
        self.canvas.delete("all")

        # grid
        for r in range(ROWS):
            for c in range(COLS):
                x,y = c*CELL, r*CELL
                color = "gray" if self.grid[r][c] else "green"
                self.canvas.create_rectangle(x,y,x+CELL,y+CELL, fill=color)

        # path
        for r,c in self.enemy.path:
            self.canvas.create_rectangle(c*CELL, r*CELL,
                                         c*CELL+CELL, r*CELL+CELL,
                                         fill="darkgreen")

        # enemy
        r,c = self.enemy.pos
        self.canvas.create_oval(c*CELL+5, r*CELL+5,
                                c*CELL+CELL-5, r*CELL+CELL-5,
                                fill="red")

        # GAME OVER display
        if self.game_over:
            self.canvas.create_text(W//2, H//2,
                                    text="GAME OVER",
                                    fill="white",
                                    font=("Arial", 30, "bold"))

    def loop(self):
        if not self.game_over:
            self.enemy.update()
            self.check_collision()

        self.draw()
        self.canvas.after(200, self.loop)

# ───────── MAIN ─────────
root = tk.Tk()
root.title("Tower Defense - Game Over")
Game(root)
root.mainloop()