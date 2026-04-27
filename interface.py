import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from jogo8 import breadth_first_search, depth_first_search, greedy_search, a_star_search

BG          = "#1E1E2E"
BG_CARD     = "#2A2A3E"
BG_INPUT    = "#313147"
ACCENT      = "#7C6AF7"
ACCENT2     = "#5DCAA5"
WARN        = "#EF9F27"
DANGER      = "#E24B4A"
TEXT        = "#E8E8F0"
TEXT_DIM    = "#888899"
TEXT_TILE   = "#FFFFFF"
TILE_NORMAL = "#3D3D58"
TILE_EMPTY  = "#252536"
TILE_MOVED  = "#4A3F12"
TILE_GOAL   = "#1A3D2E"
FONT_TITLE  = ("Segoe UI", 16, "bold")
FONT_BOLD   = ("Segoe UI", 11, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_TILE   = ("Segoe UI", 22, "bold")
FONT_MONO   = ("Consolas", 10)

ALGO_LIST = [
    ("BFS (Largura)",      breadth_first_search),
    ("DFS (Profundidade)", depth_first_search),
    ("Gulosa",             greedy_search),
    ("A*",                 a_star_search),
]

PRESETS_3 = {
    "1":   [1, 2, 3, 4, 0, 5, 7, 8, 6],
    "2":   [1, 0, 3, 4, 2, 6, 7, 5, 8],
    "3": [0, 1, 3, 5, 2, 6, 4, 7, 8],
}

PRESETS_4 = {
    "1":   [1,2,3,4,5,6,7,8,9,10,11,12,13,14,0,15],
    "2":   [1,2,3,4,5,6,7,8,9,10,11,12,13,0,14,15],
}

def make_goal(n):
    return list(range(1, n * n)) + [0]

class BoardWidget(tk.Frame):
    def __init__(self, parent, size=3, cell=52, **kw):
        super().__init__(parent, bg=BG_CARD, **kw)
        self.size = size
        self.cell = cell
        self.labels = []
        self._build()

    def _build(self):
        for w in self.winfo_children():
            w.destroy()
        self.labels = []
        for i in range(self.size * self.size):
            r, c = divmod(i, self.size)
            lbl = tk.Label(
                self, text="",
                font=FONT_TILE, bg=TILE_NORMAL, fg=TEXT_TILE,
                relief="flat", bd=0,
                width=3, height=1,
            )
            lbl.grid(row=r, column=c, padx=3, pady=3, ipadx=4, ipady=6)
            self.labels.append(lbl)

    def set_state(self, state, prev_state=None, goal=None):
        for i, v in enumerate(state):
            lbl = self.labels[i]
            if v == 0:
                lbl.config(text="", bg=TILE_EMPTY)
            else:
                lbl.config(text=str(v))
                if goal and state == goal:
                    lbl.config(bg=TILE_GOAL)
                elif prev_state and prev_state[i] != v and prev_state[i] != 0:
                    lbl.config(bg=TILE_MOVED)
                else:
                    lbl.config(bg=TILE_NORMAL)

    def resize(self, size):
        self.size = size
        self._build()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo do 8 / 15 — Buscas em IA · UFPI")
        self.configure(bg=BG)
        self.resizable(True, True)

        self.size_var = tk.IntVar(value=3)
        self.algo_vars = [tk.BooleanVar(value=True) for _ in ALGO_LIST]
        self.entries = []
        self.results = {}          
        self.step_paths = {}      
        self.current_algo = tk.StringVar()
        self.step_index = 0
        self.play_job = None
        self._running = False
        self._timer_start = 0.0
        self._timer_job = None
        self._cancel_event = threading.Event()

        self._build_ui()
        self._draw_input_grid()

    def _build_ui(self):
        tk.Label(self, text="Jogo do 8 / 15 — Buscas em IA",
                 font=FONT_TITLE, bg=BG, fg=ACCENT).pack(pady=(14, 0))

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=4)

        self._left  = tk.Frame(body, bg=BG)
        self._right = tk.Frame(body, bg=BG)
        self._left.pack(side="left", fill="y", padx=(0, 12))
        self._right.pack(side="left", fill="both", expand=True)

        self._build_left()
        self._build_right()
        self._build_bottom()

    def _build_left(self):
        p = self._left
        card = self._card(p, "Tamanho do tabuleiro")
        card.pack(fill="x", pady=(0, 8))
        row = tk.Frame(card, bg=BG_CARD)
        row.pack()
        for lbl, val in [("3×3  (Jogo do 8)", 3), ("4×4  (Jogo do 15)", 4)]:
            tk.Radiobutton(
                row, text=lbl, variable=self.size_var, value=val,
                bg=BG_CARD, fg=TEXT, selectcolor=BG_INPUT,
                activebackground=BG_CARD, font=FONT_BODY,
                command=self._on_size_change,
            ).pack(anchor="w")

        card2 = self._card(p, "Estado inicial  (0 = vazio)")
        card2.pack(fill="x", pady=(0, 8))
        self.grid_frame = tk.Frame(card2, bg=BG_CARD)
        self.grid_frame.pack(pady=4)

        self.preset_frame = tk.Frame(card2, bg=BG_CARD)
        self.preset_frame.pack(pady=(0, 4))
        self._draw_presets()

        card3 = self._card(p, "Algoritmos")
        card3.pack(fill="x", pady=(0, 8))
        for i, (name, _) in enumerate(ALGO_LIST):
            tk.Checkbutton(
                card3, text=name, variable=self.algo_vars[i],
                bg=BG_CARD, fg=TEXT, selectcolor=BG_INPUT,
                activebackground=BG_CARD, font=FONT_BODY,
            ).pack(anchor="w")

        btn_row = tk.Frame(p, bg=BG)
        btn_row.pack(fill="x", pady=(0, 6))

        self.solve_btn = tk.Button(
            btn_row, text="Resolver", font=FONT_BOLD,
            bg=ACCENT, fg="white", relief="flat",
            activebackground="#6055CC", activeforeground="white",
            cursor="hand2", pady=8,
            command=self._start_solve,
        )
        self.solve_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.cancel_btn = tk.Button(
            btn_row, text="Cancelar", font=FONT_BOLD,
            bg=DANGER, fg="white", relief="flat",
            activebackground="#AA2222", activeforeground="white",
            cursor="hand2", pady=8, state="disabled",
            command=self._cancel_solve,
        )
        self.cancel_btn.pack(side="left")
       

    def _build_right(self):
        p = self._right

        nb = ttk.Notebook(p)
        nb.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",        background=BG, borderwidth=0)
        style.configure("TNotebook.Tab",    background=BG_CARD, foreground=TEXT_DIM,
                        padding=[12, 6], font=FONT_BODY)
        style.map("TNotebook.Tab",
                  background=[("selected", BG_INPUT)],
                  foreground=[("selected", TEXT)])
        style.configure("TFrame", background=BG)

        self.tab_compare = ttk.Frame(nb)
        self.tab_steps   = ttk.Frame(nb)
        nb.add(self.tab_compare, text="  Comparar  ")
        nb.add(self.tab_steps,   text="  Passo a passo  ")

        self._build_compare_tab()
        self._build_steps_tab()
    
    def _build_bottom(self):
        footer = tk.Frame(self, bg=BG)
        footer.pack(side="bottom", fill="x", padx=16, pady=(0, 10))

        prog_card = self._card(footer, "Progresso")
        prog_card.pack(fill="x")

        self.algo_prog_lbl = tk.Label(prog_card, text="Aguardando...",
                                       font=FONT_SMALL, bg=BG_CARD, fg=WARN, anchor="w")
        self.algo_prog_lbl.pack(fill="x", padx=10, pady=(6, 0))

        self.progress_bar = ttk.Progressbar(prog_card, mode="indeterminate", length=400)
        self.progress_bar.pack(fill="x", padx=10, pady=(6, 4))

        stats_row = tk.Frame(prog_card, bg=BG_CARD)
        stats_row.pack(fill="x", padx=10, pady=(0, 5))

        self.visited_lbl = tk.Label(stats_row, text="Nós visitados: —",
                                     font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM)
        self.visited_lbl.pack(side="left", padx=(0, 20))

        self.frontier_lbl = tk.Label(stats_row, text="Máx. fronteira: —",
                                      font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM)
        self.frontier_lbl.pack(side="left", padx=(0, 20))

        self.elapsed_lbl = tk.Label(stats_row, text="Tempo decorrido: —",
                                     font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM)
        self.elapsed_lbl.pack(side="left")

        self.status_lbl = tk.Label(footer, text="", font=FONT_SMALL,
                                    bg=BG, fg=TEXT_DIM)
        self.status_lbl.pack(pady=2)

    def _build_compare_tab(self):
        p = self.tab_compare

        cols = ("Algoritmo", "Movimentos", "Nós visitados", "Máx. fronteira",
                "Prof. solução", "Prof. máx.", "Tempo (s)", "Ótimo", "Completo")

        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background=BG_CARD, foreground=TEXT,
                        fieldbackground=BG_CARD, rowheight=26,
                        font=FONT_BODY)
        style.configure("Dark.Treeview.Heading",
                        background=BG_INPUT, foreground=ACCENT,
                        font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Dark.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])

        self.tree = ttk.Treeview(p, columns=cols, show="headings",
                                 style="Dark.Treeview", height=6)
        widths = [130, 100, 100, 120, 100, 100, 100, 90, 90]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center", minwidth=60)

        sb = ttk.Scrollbar(p, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=sb.set)
        self.tree.pack(fill="x", padx=8, pady=(12, 0))
        sb.pack(fill="x", padx=8)

        leg = tk.Frame(p, bg=BG)
        leg.pack(fill="x", padx=8, pady=(10, 0))
        tk.Label(leg, text="Heurística: Distância de Manhattan  |  *DFS com limite de profundidade 32",
                 font=FONT_SMALL, bg=BG, fg=TEXT_DIM).pack(anchor="w")

    def _build_steps_tab(self):
        p = self.tab_steps

        top = tk.Frame(p, bg=BG)
        top.pack(fill="x", padx=8, pady=(10, 4))

        tk.Label(top, text="Algoritmo:", font=FONT_BODY, bg=BG, fg=TEXT_DIM).pack(side="left")
        self.algo_combo = ttk.Combobox(top, textvariable=self.current_algo,
                                       state="readonly", width=22, font=FONT_BODY)
        self.algo_combo.pack(side="left", padx=6)
        self.algo_combo.bind("<<ComboboxSelected>>", lambda e: self._load_steps())

        nav = tk.Frame(p, bg=BG)
        nav.pack(pady=4)

        btn_kw = dict(bg=BG_INPUT, fg=TEXT, relief="flat", font=FONT_BODY,
                      activebackground=ACCENT, activeforeground="white",
                      cursor="hand2", padx=10, pady=4)
        self.btn_prev  = tk.Button(nav, text="◀ Anterior", command=lambda: self._step(-1), **btn_kw)
        self.btn_next  = tk.Button(nav, text="Próximo ▶",  command=lambda: self._step(1),  **btn_kw)
        self.btn_play  = tk.Button(nav, text="▶ Auto",     command=self._toggle_play,      **btn_kw)
        self.btn_first = tk.Button(nav, text="|◀ Início",  command=lambda: self._goto(0),  **btn_kw)
        self.btn_last  = tk.Button(nav, text="Fim ▶|",     command=lambda: self._goto(-1), **btn_kw)

        self.btn_first.grid(row=0, column=0, padx=3)
        self.btn_prev.grid(row=0,  column=1, padx=3)
        self.btn_play.grid(row=0,  column=2, padx=3)
        self.btn_next.grid(row=0,  column=3, padx=3)
        self.btn_last.grid(row=0,  column=4, padx=3)

        self.step_lbl = tk.Label(p, text="", font=FONT_BODY, bg=BG, fg=TEXT_DIM)
        self.step_lbl.pack(pady=(2, 6))

        boards = tk.Frame(p, bg=BG)
        boards.pack()

        tk.Label(boards, text="Estado atual", font=FONT_SMALL, bg=BG, fg=TEXT_DIM).grid(row=0, column=0, pady=(0,4))
        tk.Label(boards, text="→", font=("Segoe UI", 20), bg=BG, fg=TEXT_DIM).grid(row=1, column=1, padx=12)
        tk.Label(boards, text="Próximo estado", font=FONT_SMALL, bg=BG, fg=TEXT_DIM).grid(row=0, column=2, pady=(0,4))

        self.board_cur = BoardWidget(boards, size=3)
        self.board_nxt = BoardWidget(boards, size=3)
        self.board_cur.grid(row=1, column=0)
        self.board_nxt.grid(row=1, column=2)

        self.move_lbl = tk.Label(p, text="", font=FONT_BODY, bg=BG, fg=WARN, wraplength=420)
        self.move_lbl.pack(pady=(8, 4))

        self.step_console = tk.Text(p, height=5, font=FONT_MONO,
                                    bg=BG_CARD, fg=TEXT_DIM, relief="flat",
                                    state="disabled", wrap="word")
        self.step_console.pack(fill="x", padx=8, pady=(0, 8))

    def _card(self, parent, title):
        frame = tk.LabelFrame(parent, text=f"  {title}  ",
                              font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM,
                              relief="flat", bd=1, labelanchor="nw",
                              highlightthickness=1,
                              highlightbackground=BG_INPUT)
        return frame

    def _status(self, msg, color=TEXT_DIM):
        self.status_lbl.config(text=msg, fg=color)

    def _draw_input_grid(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.entries = []
        n = self.size_var.get()
        for i in range(n * n):
            r, c = divmod(i, n)
            e = tk.Entry(self.grid_frame, width=3, font=FONT_TILE,
                         justify="center", bg=BG_INPUT, fg=TEXT,
                         insertbackground=TEXT, relief="flat", bd=0)
            e.grid(row=r, column=c, padx=3, pady=3, ipadx=4, ipady=4)
            self.entries.append(e)

    def _draw_presets(self):
        for w in self.preset_frame.winfo_children():
            w.destroy()
        presets = PRESETS_3 if self.size_var.get() == 3 else PRESETS_4
        tk.Label(self.preset_frame, text="Presets:", font=FONT_SMALL,
                 bg=BG_CARD, fg=TEXT_DIM).pack(side="left", padx=(0, 4))
        for name, vals in presets.items():
            tk.Button(
                self.preset_frame, text=name, font=FONT_SMALL,
                bg=BG_INPUT, fg=TEXT, relief="flat",
                activebackground=ACCENT, activeforeground="white",
                cursor="hand2", padx=6, pady=2,
                command=lambda v=vals: self._load_preset(v),
            ).pack(side="left", padx=2)

    def _on_size_change(self):
        self._draw_input_grid()
        self._draw_presets()
        self.results = {}
        self.step_paths = {}
        self._clear_compare()
        self._set_progress_labels(0, 0, 0.0)

    def _load_preset(self, vals):
        for e, v in zip(self.entries, vals):
            e.delete(0, "end")
            e.insert(0, str(v))

    def _update_progress(self, visited, maxF, maxD):
        elapsed = time.time() - self._timer_start
        self.after(0, lambda v=visited, f=maxF, e=elapsed: self._set_progress_labels(v, f, e))

    def _set_progress_labels(self, visited, maxF, elapsed):
        self.visited_lbl.config(text="Nós visitados: " + str(visited))
        self.frontier_lbl.config(text="Máx. fronteira: " + str(maxF))
        self.elapsed_lbl.config(text="Tempo decorrido: " + str(round(elapsed, 1)) + "s")

    def _tick_elapsed(self):
        if not self._running:
            return
        elapsed = time.time() - self._timer_start
        self.elapsed_lbl.config(text="Tempo decorrido: " + str(round(elapsed, 1)) + "s")
        self._timer_job = self.after(100, self._tick_elapsed)

    def _read_board(self):
        n = self.size_var.get()
        try:
            vals = [int(e.get()) for e in self.entries]
        except ValueError:
            raise ValueError("Insira apenas números inteiros em todas as células.")
        expected = set(range(n * n))
        if set(vals) != expected:
            raise ValueError(f"O tabuleiro deve ter exatamente os números 0 a {n*n-1} sem repetição.")
        return vals

    def _start_solve(self):
        try:
            board = self._read_board()            
        except ValueError as e:
            messagebox.showerror("Erro de entrada", str(e))
            return

        selected = [(name, fn) for (name, fn), var in zip(ALGO_LIST, self.algo_vars) if var.get()]
        if not selected:
            messagebox.showwarning("Aviso", "Selecione pelo menos um algoritmo.")
            return

        self._running = True
        self._cancel_event.clear()
        self.solve_btn.config(state="disabled", text="Rodando…")
        self.cancel_btn.config(state="normal") 
        self.progress_bar.start(12)
        self.algo_prog_lbl.config(text="Executando algoritmos...")
        self._status("Executando algoritmos, aguarde…", WARN)
        self.results = {}
        self.step_paths = {}
        self._clear_compare()
        self._timer_start = time.time()
        self._tick_elapsed()

        threading.Thread(target=self._run_algos, args=(board, selected), daemon=True).start()

    def _cancel_solve(self):
        self._running = False
        self._cancel_event.set()
        if self._timer_job:
            self.after_cancel(self._timer_job)
            self._timer_job = None
        self.solve_btn.config(state="normal", text="Resolver")
        self.cancel_btn.config(state="disabled")
        self.progress_bar.stop()
        self.algo_prog_lbl.config(text="Cancelado.")
        self._status("Busca interrompida.", DANGER)

    def _run_algos(self, board, selected):
        goal = make_goal(self.size_var.get())
        for name, fn in selected:
            if self._cancel_event.is_set():
                break
            self.after(0, lambda n=name: self._status(f"Rodando {n}…", WARN))
            self.after(0, lambda n=name: self.algo_prog_lbl.config(text="Algoritmo atual: " + n))
            t0 = time.time()
            res = fn(board, goal, self._update_progress, self._cancel_event)
            elapsed = time.time() - t0

            if res and res[0]:
                node, visited, maxF, maxD = res
                path = node.get_path()
                self.results[name] = {
                    "node": node, "visited": visited, "maxF": maxF,
                    "maxD": maxD, "path": path,
                    "moves": len(path) - 1, "time": elapsed,
                }
                self.step_paths[name] = path
            else:
                self.results[name] = None

        self.after(0, self._on_done)

    def _on_done(self):
        self._running = False
        if self._timer_job:
            self.after_cancel(self._timer_job)
            self._timer_job = None

        self.progress_bar.stop()
        self.solve_btn.config(state="normal", text="▶  Resolver")
        self.cancel_btn.config(state="disabled")
        if self._cancel_event.is_set():
            self.algo_prog_lbl.config(text="Cancelado")
            self._status("Busca interrompida.", DANGER)
        else:
            self.algo_prog_lbl.config(text="Concluído")
            self._status("Concluído.", ACCENT2)
        self._fill_compare()
        self._setup_steps()

    def _clear_compare(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def _fill_compare(self):
        self._clear_compare()
        found = {k: v for k, v in self.results.items() if v}
        if not found:
            self._status("Nenhum algoritmo encontrou solução.", DANGER)
            return

        best_moves   = min(v["moves"]   for v in found.values())
        best_visited = min(v["visited"] for v in found.values())
        best_maxF    = min(v["maxF"]    for v in found.values())

        for name, r in self.results.items():
            otimo = "Sim" if r and r.get("moves") == best_moves else "Não"
            completo = "Sim" if r and r.get("node") else "Não"
            if r is None:
                self.tree.insert("", "end", tags=("nosol",),
                    values=(name, "—", "—", "—", "—", "—", "—", otimo, completo))
            else:
                tag = "best" if (r["moves"] == best_moves and
                                  r["visited"] == best_visited) else "normal"
                self.tree.insert("", "end", tags=(tag,),
                    values=(
                        name,
                        r["moves"],
                        r["visited"],
                        r["maxF"],
                        r["node"].depth,
                        r["maxD"],
                        f"{r['time']:.4f}",
                        otimo,
                        completo,
                    ))

    def _setup_steps(self):
        names = [k for k, v in self.results.items() if v]
        if not names:
            return
        self.algo_combo["values"] = names
        self.algo_combo.set(names[0])
        self.current_algo.set(names[0])

        n = self.size_var.get()
        self.board_cur.resize(n)
        self.board_nxt.resize(n)
        self._load_steps()

    def _load_steps(self):
        name = self.current_algo.get()
        if name not in self.step_paths:
            return
        self.step_index = 0
        self._stop_play()
        self._render_step()

    def _render_step(self):
        name = self.current_algo.get()
        path = self.step_paths.get(name, [])
        if not path:
            return

        total = len(path)
        i = self.step_index
        goal = make_goal(self.size_var.get())

        cur = path[i]
        prev = path[i - 1] if i > 0 else None
        nxt  = path[i + 1] if i < total - 1 else None

        self.board_cur.set_state(cur, prev, goal)
        if nxt:
            self.board_nxt.set_state(nxt, cur, goal)
            moved = next((cur[j] for j in range(len(cur)) if cur[j] != nxt[j] and cur[j] != 0), None)
            self.move_lbl.config(text=f"Peça {moved} se move para a posição vazia." if moved else "")
        else:
            self.board_nxt.set_state(goal, cur, goal)
            self.move_lbl.config(text="✔ Estado objetivo alcançado!")

        self.step_lbl.config(
            text=f"Passo {i + 1} / {total}  —  {self.results[name]['moves']} movimentos no total"
        )

        self.step_console.config(state="normal")
        self.step_console.delete("1.0", "end")
        n = self.size_var.get()
        lines = [f"  Estado {i + 1}:"]
        for row in range(n):
            linha = "  " + "  ".join(f"{cur[row*n+c]:2}" for c in range(n))
            lines.append(linha)
        if nxt:
            lines.append(f"\n  Próximo:")
            for row in range(n):
                linha = "  " + "  ".join(f"{nxt[row*n+c]:2}" for c in range(n))
                lines.append(linha)
        self.step_console.insert("end", "\n".join(lines))
        self.step_console.config(state="disabled")

        self.btn_prev.config(state="normal" if i > 0 else "disabled")
        self.btn_next.config(state="normal" if i < total - 1 else "disabled")
        self.btn_first.config(state="normal" if i > 0 else "disabled")
        self.btn_last.config(state="normal" if i < total - 1 else "disabled")

    def _step(self, delta):
        name = self.current_algo.get()
        path = self.step_paths.get(name, [])
        self.step_index = max(0, min(len(path) - 1, self.step_index + delta))
        self._render_step()

    def _goto(self, idx):
        name = self.current_algo.get()
        path = self.step_paths.get(name, [])
        self.step_index = idx if idx >= 0 else len(path) - 1
        self._render_step()

    def _toggle_play(self):
        if not self.current_algo.get():
            return # Nada para reproduzir
        if self.play_job:
            self._stop_play()
        else:
            self.btn_play.config(text="⏸ Pausar", bg=WARN, fg=BG)
            self._auto_play()

    def _auto_play(self):
        name = self.current_algo.get()
        path = self.step_paths.get(name, [])
        if self.step_index >= len(path) - 1:
            self._stop_play()
            return
        self._step(1)
        self.play_job = self.after(600, self._auto_play)

    def _stop_play(self):
        if self.play_job:
            self.after_cancel(self.play_job)
            self.play_job = None
        self.btn_play.config(text="▶ Auto", bg=BG_INPUT, fg=TEXT)


if __name__ == "__main__":
    app = App()
    app.mainloop()