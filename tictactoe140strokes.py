import tkinter as tk, random

# все выигрышные тройки клеток (индексы 0..8)
WIN = [(0,1,2),(3,4,5),(6,7,8),
       (0,3,6),(1,4,7),(2,5,8),
       (0,4,8),(2,4,6)]

class TicTacToeApp:
    def __init__(self, root):  # инициализация UI 
        self.root = root
        root.title("Крестики-нолики - minimax")
        self.SIZE, self.MARGIN = 540, 24
        self.CELL = (self.SIZE - 2*self.MARGIN) // 3

        self.board = [" "]*9
        self.game_over = False
        self.human = tk.StringVar(value="X")
        self.difficulty = tk.StringVar(value="Сложная")

        left = tk.Frame(root); left.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)
        tk.Label(left, text="Настройки", font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Button(left, text="Новая игра", command=self.start).pack(anchor="w", pady=4)

        who = tk.Frame(left); who.pack(anchor="w", pady=4)
        tk.Label(who, text="Вы играете:").pack(side=tk.LEFT)
        [tk.Radiobutton(who, text=p, variable=self.human, value=p).pack(side=tk.LEFT) for p in "XO"]

        diff = tk.Frame(left); diff.pack(anchor="w", pady=4)
        tk.Label(diff, text="Сложность:").pack(side=tk.LEFT)
        tk.OptionMenu(diff, self.difficulty, "Лёгкая", "Средняя", "Сложная").pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Нажмите «Новая игра».")
        tk.Label(left, textvariable=self.status_var, wraplength=200, justify="left").pack(anchor="w", pady=6)

        self.canvas = tk.Canvas(root, width=self.SIZE, height=self.SIZE, bg="#fff", highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=8, pady=8)
        self.canvas.bind("<Button-1>", self.handle_click)

        self.draw_board()

    def start(self):  # сброс игры и старт по выбору X/O
        self.game_over = False
        self.board = [" "]*9
        self.draw_board()
        self.set_status()
        if self.human.get() == "O":
            self.ai_move()

    def set_status(self, text=None):  # обновление строки статуса
        if text:
            self.status_var.set(text); return
        if not self.game_over:
            self.status_var.set(f"Ход: {self.current_turn()} • {self.difficulty.get()}")

    def draw_board(self):  # перерисовка сетки и фигур
        c = self.canvas; c.delete("all")
        x0 = y0 = self.MARGIN; x1 = y1 = self.SIZE - self.MARGIN
        for i in range(1, 3):
            x = x0 + i*self.CELL; y = y0 + i*self.CELL
            c.create_line(x, y0, x, y1, width=4, fill="#cbd5e1")
            c.create_line(x0, y, x1, y, width=4, fill="#cbd5e1")
        for i, ch in enumerate(self.board):
            if ch != " ":
                self.draw_symbol(i, ch)

    def draw_symbol(self, idx, ch):  # рисование X или O в клетке 
        r, col = divmod(idx, 3)
        x0 = self.MARGIN + col*self.CELL; y0 = self.MARGIN + r*self.CELL
        x1 = x0 + self.CELL; y1 = y0 + self.CELL
        pad, w = int(self.CELL*0.18), 8
        if ch == "X":
            self.canvas.create_line(x0+pad, y0+pad, x1-pad, y1-pad, width=w, fill="#ef4444", capstyle=tk.ROUND)
            self.canvas.create_line(x0+pad, y1-pad, x1-pad, y0+pad, width=w, fill="#ef4444", capstyle=tk.ROUND)
        else:
            self.canvas.create_oval(x0+pad, y0+pad, x1-pad, y1-pad, width=w, outline="#2563eb")

    def current_turn(self):  # чей ход сейчас: 'X' или 'O'
        return "X" if self.board.count("X") == self.board.count("O") else "O"

    def handle_click(self, e):  # обработчик клика по полю
        if self.game_over or self.current_turn() != self.human.get(): return
        r = (e.y - self.MARGIN) // self.CELL; col = (e.x - self.MARGIN) // self.CELL
        if r not in range(3) or col not in range(3): return
        idx = r*3 + col
        if self.board[idx] != " ": return
        self.place(idx, self.human.get())
        if self.end_check(): return
        self.root.after(80, self.ai_move)

    def place(self, idx, ch):  # поставить символ и обновить UI
        self.board[idx] = ch
        self.draw_board()
        self.set_status()

    def ai_move(self):  # ход компьютера с учётом сложности
        if self.game_over: return
        move = choose_best_move(self.board, self.ai_symbol(), self.human.get(), self.difficulty.get())
        if move is not None:
            self.place(move, self.ai_symbol())
        self.end_check()

    def ai_symbol(self):  # символ ИИ: противоположный человеку
        return "O" if self.human.get() == "X" else "X"

    def end_check(self):  # проверка конца игры и сообщение
        w, _ = check_winner(self.board)
        if w:
            self.game_over = True
            self.set_status("Вы выиграли! 🎉" if w == self.human.get() else "ИИ выиграл =).")
            return True
        if " " not in self.board:
            self.game_over = True
            self.set_status("Ничья.")
            return True
        return False

def check_winner(board):  # возврат ('X'/'O' или None None)
    for a, b, c in WIN:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a], (a, c)
    return None, None

def is_terminal(board, ai, hu):  # терминальная ли позиция для minimax
    w, _ = check_winner(board)
    if w == ai: return True, 1
    if w == hu: return True, -1
    if " " not in board: return True, 0
    return False, None

def evaluate(board, ai, hu):  # эвристика для обрезанной глубины
    score = 0
    for a, b, c in WIN:
        line = [board[a], board[b], board[c]]
        if ai in line and hu in line: continue
        ac, hc = line.count(ai), line.count(hu)
        if hc == 0: score += [0, 1, 10, 100][ac]
        if ac == 0: score -= [0, 1, 10, 100][hc]
    if board[4] == ai: score += 2
    if board[4] == hu: score -= 2
    return score

def choose_best_move(board, ai, hu, diff):  # выбор хода с учётом сложности
    empties = [i for i, v in enumerate(board) if v == " "]
    if not empties: return None
    if diff == "Лёгкая":
        if random.random() < 0.4:
            m = win_or_block(board, ai, hu)
            if m is not None: return m
        return random.choice(empties)
    if diff == "Средняя":
        m = win_or_block(board, ai, hu)
        return m if m is not None else best_move_minimax(board, ai, hu, lim=3)
    m = win_or_block(board, ai, hu)
    if m is not None: return m
    if board[4] == " ": return 4
    return best_move_minimax(board, ai, hu, lim=None)

def win_or_block(board, ai, hu):  # мгновенно выиграть или перекрыть соперника
    for i in range(9):
        if board[i] == " ":
            board[i] = ai; w, _ = check_winner(board); board[i] = " "
            if w == ai: return i
    for i in range(9):
        if board[i] == " ":
            board[i] = hu; w, _ = check_winner(board); board[i] = " "
            if w == hu: return i
    return None

def best_move_minimax(board, ai, hu, lim):  # minimax для ИИ
    best_score, best_mv = -10**9, None
    for i in range(9):
        if board[i] == " ":
            board[i] = ai
            sc = minimax(board, 0, False, ai, hu, -10**9, 10**9, lim)
            board[i] = " "
            if sc > best_score: best_score, best_mv = sc, i
    return best_mv

def minimax(board, depth, is_max, ai, hu, alpha, beta, lim):  # рекурсивный поиск оптимального хода с α-β
    done, val = is_terminal(board, ai, hu)
    if done: return val * (1000 - depth*10)
    if lim is not None and depth >= lim: return evaluate(board, ai, hu)
    if is_max:
        best = -10**9
        for i in range(9):
            if board[i] == " ":
                board[i] = ai
                best = max(best, minimax(board, depth+1, False, ai, hu, alpha, beta, lim))
                board[i] = " "
                alpha = max(alpha, best)
                if beta <= alpha: break
        return best
    else:
        best = 10**9
        for i in range(9):
            if board[i] == " ":
                board[i] = hu
                best = min(best, minimax(board, depth+1, True, ai, hu, alpha, beta, lim))
                board[i] = " "
                beta = min(beta, best)
                if beta <= alpha: break
        return best

if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()
