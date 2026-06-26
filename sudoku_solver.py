import tkinter as tk
from tkinter import messagebox, ttk
import time
import random
import os
import json

class SudokuQuantumPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Retro Edition")
        
        # Window base configuration (Supports maximize button)
        self.root.geometry("520x860")
        
        # Save-File Path Settings
        self.save_file = "quantum_profile.json"
        
        # Default Profile Variables
        self.player_name = "Player 1"
        self.current_theme = "pink"
        self.grid_size = 4 
        self.is_daily_challenge = False
        self.total_points = 500  
        self.solve_streak = 0
        self.session_history = []
        
        self.load_profile_from_disk()
        
        # High-Vibrancy Neon Retro & High-Contrast Light Templates
        self.themes = {
            "pink": {"bg": "#0D0208", "card": "#1A0510", "fg": "#FFFFFF", "accent": "#00FF66", "sub": "#2D0B1E", "cell_bg": "#15030C", "err": "#FF1E56", "grid_line": "#FF2A85", "exit_bg": "#2D0B1E"},
            "orange": {"bg": "#0A0300", "card": "#1C0A00", "fg": "#FFFFFF", "accent": "#00FF66", "sub": "#331400", "cell_bg": "#140600", "err": "#FF3333", "grid_line": "#FF6B00", "exit_bg": "#331400"},
            "cyan": {"bg": "#00050A", "card": "#001220", "fg": "#FFFFFF", "accent": "#00FF66", "sub": "#00223D", "cell_bg": "#000B14", "err": "#FF2255", "grid_line": "#00E5FF", "exit_bg": "#00223D"},
            "emerald": {"bg": "#000803", "card": "#001A0A", "fg": "#FFFFFF", "accent": "#FF2A85", "sub": "#003314", "cell_bg": "#000F05", "err": "#FF3344", "grid_line": "#00FF66", "exit_bg": "#003314"},
            "white": {"bg": "#F5F5F7", "card": "#FFFFFF", "fg": "#1D1D1F", "accent": "#0088CC", "sub": "#E5E5EA", "cell_bg": "#F2F2F7", "err": "#FF3B30", "grid_line": "#8E8E93", "exit_bg": "#D1D1D6"}
        }
        
        self.start_time = 0
        self.timer_running = False
        self.auto_solved = False 
        self.cells = [] 
        
        # Outer parent frame configuration handles wide window resizing gracefully
        self.screen_wrapper = tk.Frame(self.root)
        self.screen_wrapper.pack(fill="both", expand=True)
        self.screen_wrapper.grid_rowconfigure(0, weight=1)
        self.screen_wrapper.grid_columnconfigure(0, weight=1)
        
        self.main_container = None
        self.show_title_screen()

    def build_enclosed_canvas_box(self):
        """Forces the main UI layout to remain centered within a sleek box format on wide screens."""
        if self.main_container:
            self.main_container.destroy()
            
        c = self.get_colors()
        self.root.config(bg="#050103" if self.current_theme != "white" else "#E5E5EA") 
        self.screen_wrapper.config(bg="#050103" if self.current_theme != "white" else "#E5E5EA")
        
        # Core portrait alignment containment panel box
        self.main_container = tk.Frame(
            self.screen_wrapper, bg=c["bg"], width=500, height=840,
            highlightbackground=c["grid_line"], highlightthickness=2
        )
        self.main_container.grid(row=0, column=0, sticky="")
        self.main_container.pack_propagate(False)

    def save_profile_to_disk(self):
        try:
            data = {
                "player_name": self.player_name,
                "current_theme": self.current_theme,
                "total_points": self.total_points,
                "solve_streak": self.solve_streak,
                "session_history": self.session_history
            }
            with open(self.save_file, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Data Save Issue: {e}")

    def load_profile_from_disk(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as f:
                    data = json.load(f)
                    self.player_name = data.get("player_name", "Player 1")
                    self.current_theme = data.get("current_theme", "pink")
                    self.total_points = data.get("total_points", 500)
                    self.solve_streak = data.get("solve_streak", 0)
                    self.session_history = data.get("session_history", [])
            except Exception as e:
                print(f"Profile Read Error: {e}")

    def get_colors(self):
        return self.themes.get(self.current_theme, self.themes["pink"])

    def get_subgrid_dims(self):
        if self.grid_size == 4: return (2, 2)
        if self.grid_size == 6: return (2, 3)
        return (3, 3)

    def draw_status_ribbon(self, parent_frame):
        c = self.get_colors()
        ribbon = tk.Frame(parent_frame, bg=c["card"], highlightbackground=c["grid_line"], highlightthickness=1)
        ribbon.pack(fill="x", padx=15, pady=(10, 5))
        
        tk.Label(ribbon, text=f"👤 {self.player_name.upper()}", font=("Courier New", 9, "bold"), fg=c["fg"], bg=c["card"]).pack(side="left", padx=10, pady=5)
        tk.Label(ribbon, text=f"🔥 STREAK: {self.solve_streak}D", font=("Courier New", 9, "bold"), fg="#FFD700" if self.current_theme != "white" else "#D9A700", bg=c["card"]).pack(side="left", padx=10)
        tk.Label(ribbon, text=f"⚡ {self.total_points} PTS", font=("Courier New", 10, "bold"), fg=c["accent"], bg=c["card"]).pack(side="right", padx=10)

    def draw_global_exit_anchor(self, parent_frame):
        """Injects a standardized secure exit button at the bottom base row."""
        c = self.get_colors()
        exit_bar = tk.Frame(parent_frame, bg=c["bg"])
        exit_bar.pack(side="bottom", fill="x", pady=(5, 12))
        
        btn_exit = tk.Button(
            exit_bar, text="✕ QUIT GAME STATION", font=("Courier New", 9, "bold"),
            bg=c["exit_bg"], fg="#FF1E56" if self.current_theme != "white" else "#FF3B30", bd=1, relief="solid",
            highlightthickness=0, activebackground=c["err"], activeforeground="white",
            command=self.trigger_secure_exit_flow
        )
        btn_exit.pack(padx=20, fill="x", ipady=3)

    def trigger_secure_exit_flow(self):
        """Asks for confirmation before quitting the game application completely."""
        ans = messagebox.askyesno("Quit Game", "Do you want to exit the puzzle game completely?")
        if ans:
            self.root.destroy()

    # --- VIEW 1: MAIN MENU TERMINAL ---
    def show_title_screen(self):
        self.build_enclosed_canvas_box()
        c = self.get_colors()
        
        self.draw_global_exit_anchor(self.main_container)
        
        title_bar = tk.Frame(self.main_container, bg=c["card"], height=80, highlightbackground=c["grid_line"], highlightthickness=1)
        title_bar.pack(fill="x", padx=15, pady=(20, 5))
        title_bar.pack_propagate(False)
        
        tk.Label(title_bar, text="SUDOKU RETRO EDITION", font=("Courier New", 18, "bold"), fg=c["grid_line"] if self.current_theme != "white" else c["fg"], bg=c["card"]).pack(pady=(12, 0))
        tk.Label(title_bar, text="R E T R O   A R C A D E   E N G I N E", font=("Courier New", 8), fg=c["fg"], bg=c["card"]).pack()

        self.draw_status_ribbon(self.main_container)

        menu_card = tk.Frame(self.main_container, bg=c["card"], padx=20, pady=10, highlightbackground=c["grid_line"], highlightthickness=1)
        menu_card.pack(padx=15, pady=10, fill="both", expand=True)
        
        tk.Label(menu_card, text="ENTER PLAYER NAME:", font=("Courier New", 9, "bold"), fg=c["fg"], bg=c["card"]).pack(pady=4)
        name_entry = tk.Entry(menu_card, font=("Courier New", 11), bg=c["sub"], fg=c["fg"], bd=0, insertbackground=c["fg"], justify="center", width=20)
        name_entry.insert(0, self.player_name)
        name_entry.pack(pady=4, ipady=4)
        
        tk.Label(menu_card, text="SELECT BOARD SIZE MODE:", font=("Courier New", 9, "bold"), fg=c["fg"], bg=c["card"]).pack(pady=(12, 4))
        dim_frame = tk.Frame(menu_card, bg=c["card"])
        dim_frame.pack()
        for size in [4, 6, 9]:
            btn_text = f"{size}x{size}"
            bg_col = c["grid_line"] if self.grid_size == size else c["sub"]
            fg_col = "white" if self.grid_size == size else c["fg"]
            tk.Button(dim_frame, text=btn_text, font=("Courier New", 9, "bold"), bg=bg_col, fg=fg_col, bd=0, padx=12, pady=5, command=lambda s=size: self.set_grid_size(s)).grid(row=0, column=[4,6,9].index(size), padx=4)

        tk.Label(menu_card, text="SELECT GAME THEME COLOR:", font=("Courier New", 9, "bold"), fg=c["fg"], bg=c["card"]).pack(pady=(12, 4))
        
        dd_panel = tk.Frame(menu_card, bg=c["sub"], bd=1, relief="solid")
        dd_panel.pack(pady=4, ipady=2)
        
        theme_names = {"PINK RETRO": "pink", "ORANGE ARCADE": "orange", "NEON BLUE SYSTEM": "cyan", "EMERALD GREEN LABS": "emerald", "WHITE LUX COMBINATION": "white"}
        current_display = [k for k, v in theme_names.items() if v == self.current_theme][0]
        
        lbl_dd = tk.Label(dd_panel, text=f"  {current_display}   ▼  ", font=("Courier New", 9, "bold"), bg=c["sub"], fg=c["grid_line"] if self.current_theme != "white" else c["fg"], width=24, cursor="hand2")
        lbl_dd.pack()
        
        def toggle_dropdown_menu(e):
            pop = tk.Menu(self.root, tearoff=0, background=c["sub"], foreground=c["fg"], activebackground=c["grid_line"], activeforeground="white", bd=0)
            for t_title, t_key in theme_names.items():
                pop.add_command(label=t_title, command=lambda k=t_key: self.set_theme(k))
            pop.post(lbl_dd.winfo_rootx(), lbl_dd.winfo_rooty() + lbl_dd.winfo_height())
        lbl_dd.bind("<Button-1>", toggle_dropdown_menu)

        def proceed(daily=False):
            self.player_name = name_entry.get().strip() or "Player 1"
            self.is_daily_challenge = daily
            self.save_profile_to_disk()
            self.show_game_screen()

        tk.Button(menu_card, text="START NEW GAME", font=("Courier New", 11, "bold"), bg=c["grid_line"] if self.current_theme != "white" else "#0088CC", fg="white", padx=20, pady=8, bd=0, command=lambda: proceed(daily=False)).pack(pady=(15, 4))
        tk.Button(menu_card, text="📅 PLAY DAILY CHALLENGE", font=("Courier New", 10, "bold"), bg="#FFD700" if self.current_theme != "white" else "#D9A700", fg="black", padx=15, pady=6, bd=0, command=lambda: proceed(daily=True)).pack(pady=4)
        tk.Button(menu_card, text="OPEN SCORE & HISTORY STATS", font=("Courier New", 8, "bold"), bg=c["sub"], fg=c["fg"], bd=1, padx=10, pady=4, command=self.show_dashboard_screen).pack(pady=5)

    def set_theme(self, theme_name):
        self.current_theme = theme_name
        self.save_profile_to_disk()
        self.show_title_screen()

    def set_grid_size(self, size):
        self.grid_size = size
        self.show_title_screen()

    # --- VIEW 2: GAMEPLAY WORKSPACE ---
    def show_game_screen(self):
        self.build_enclosed_canvas_box()
        c = self.get_colors()
        
        self.draw_global_exit_anchor(self.main_container)
        self.draw_status_ribbon(self.main_container)
        
        game_card = tk.Frame(self.main_container, bg=c["card"], padx=10, pady=10, highlightbackground=c["grid_line"], highlightthickness=1)
        game_card.pack(padx=15, pady=5, fill="both", expand=True)
        
        header = tk.Frame(game_card, bg=c["card"])
        header.pack(fill="x", pady=(0, 2))
        
        mode_label = "DAILY LEVEL MODE" if self.is_daily_challenge else f"CUSTOM PUZZLE MATCH"
        tk.Label(header, text=mode_label, font=("Courier New", 9, "bold"), fg=c["grid_line"] if self.current_theme != "white" else c["fg"], bg=c["card"]).pack(side="left")
        self.timer_label = tk.Label(header, text="TIME: 00:00", font=("Courier New", 9, "bold"), fg=c["fg"], bg=c["card"])
        self.timer_label.pack(side="right")
        
        prog_container = tk.Frame(game_card, bg=c["card"])
        prog_container.pack(fill="x", pady=(2, 8))
        tk.Label(prog_container, text="PROGRESS:", font=("Courier New", 8, "bold"), fg=c["fg"], bg=c["card"]).pack(side="left", padx=(0, 5))
        self.ui_progress_bar = tk.Canvas(prog_container, width=240, height=8, bg=c["sub"], highlightthickness=0)
        self.ui_progress_bar.pack(side="left", fill="x", expand=True)
        self.ui_progress_fill = self.ui_progress_bar.create_rectangle(0, 0, 0, 8, fill=c["accent"], width=0)
        
        # Grid Housing Box Enclosure Keep display locked securely
        box_frame = tk.Frame(game_card, bg=c["sub"], padx=8, pady=8, highlightbackground=c["grid_line"], highlightthickness=1)
        box_frame.pack(pady=5)
        
        grid_outer = tk.Frame(box_frame, bg=c["grid_line"], bd=1)
        grid_outer.pack()
        
        self.cells = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        box_rows, box_cols = self.get_subgrid_dims()
        
        cell_font_size = 16 if self.grid_size == 4 else (13 if self.grid_size == 6 else 11)
        cell_width = 3 if self.grid_size == 4 else 2
        
        for r in range(self.grid_size):
            for col in range(self.grid_size):
                padx = (2 if col % box_cols == 0 and col > 0 else 0, 0)
                pady = (2 if r % box_rows == 0 and r > 0 else 0, 0)
                
                cell_box = tk.Frame(grid_outer, bg=c["bg"])
                cell_box.grid(row=r, column=col, padx=padx, pady=pady)
                
                vcmd = (self.root.register(self.validate_cell), '%P')
                entry = tk.Entry(
                    cell_box, width=cell_width, font=("Courier New", cell_font_size, "bold"),
                    bg=c["cell_bg"], fg=c["fg"], justify="center", bd=0,
                    insertbackground=c["fg"], validate="key", validatecommand=vcmd
                )
                entry.pack(padx=1, pady=1, ipady=6)
                entry.bind("<KeyRelease>", lambda e, row=r, col_idx=col: self.on_cell_change(row, col_idx))
                self.cells[r][col] = entry

        control_frame = tk.Frame(game_card, bg=c["card"])
        control_frame.pack(fill="x", pady=5)
        
        tk.Button(control_frame, text="Auto Solve", font=("Courier New", 8, "bold"), bg=c["sub"], fg=c["fg"], bd=1, command=self.trigger_solver).grid(row=0, column=0, padx=2, sticky="ew")
        tk.Button(control_frame, text="Submit Score", font=("Courier New", 8, "bold"), bg=c["grid_line"] if self.current_theme != "white" else "#0088CC", fg="white", bd=0, command=self.evaluate_user_game).grid(row=0, column=1, padx=2, sticky="ew")
        tk.Button(control_frame, text="Clear All", font=("Courier New", 8, "bold"), bg="#FF1E56" if self.current_theme != "white" else "#FF3B30", fg="white", bd=0, command=self.clear_grid).grid(row=0, column=2, padx=2, sticky="ew")
        control_frame.columnconfigure((0,1,2), weight=1)
        
        hint_shop_frame = tk.Frame(game_card, bg=c["sub"], padx=4, pady=4)
        hint_shop_frame.pack(fill="x", pady=2)
        
        self.btn_hint = tk.Button(hint_shop_frame, text="💡 BUY HINT (-100 PTS)", font=("Courier New", 8, "bold"), bg=c["card"], fg="#FFD700" if self.current_theme != "white" else "#D9A700", bd=0, command=self.purchase_smart_hint)
        self.btn_hint.pack(side="left", fill="x", expand=True)
        
        tk.Button(hint_shop_frame, text="⚡ FLASH PEEK", font=("Courier New", 8, "bold"), bg=c["card"], fg=c["fg"], bd=0, command=self.trigger_tachyon_flash).pack(side="right", padx=(4,0))

        if not self.is_daily_challenge:
            tk.Button(game_card, text="GENERATE RANDOM PUZZLE BOARD", font=("Courier New", 8, "bold"), bg=c["sub"], fg=c["fg"], bd=1, command=self.inject_random_generated_game).pack(fill="x", pady=2)
        else:
            self.inject_daily_challenge_blueprint()
            
        tk.Button(game_card, text="📊 STATS & TROPHY DASHBOARD", font=("Courier New", 9, "bold"), bg="#00FF66" if self.current_theme != "white" else "#34C759", fg="black" if self.current_theme != "white" else "white", bd=0, pady=4, command=self.show_dashboard_screen).pack(fill="x", pady=4)
        tk.Button(game_card, text="← Return to Main Menu", font=("Courier New", 8, "underline"), bg=c["card"], fg=c["fg"], bd=0, command=self.show_title_screen).pack(pady=2)
        
        self.start_timer()

    def validate_cell(self, text):
        if text == "": return True
        valid_chars = "1234" if self.grid_size == 4 else ("123456" if self.grid_size == 6 else "123456789")
        return len(text) == 1 and text in valid_chars

    def on_cell_change(self, row, col):
        self.update_live_progress_bar()
        self.check_realtime_conflicts()
        
        total_slots = self.grid_size * self.grid_size
        filled = sum(1 for r in range(self.grid_size) for c in range(self.grid_size) if self.cells[r][c].get() != "")
        if filled == total_slots:
            self.root.after(300, self.evaluate_user_game)

    def check_realtime_conflicts(self):
        c = self.get_colors()
        board = self.get_matrix_from_gui()
        for r in range(self.grid_size):
            for col in range(self.grid_size):
                self.cells[r][col].config(bg=c["cell_bg"])

        for r in range(self.grid_size):
            for col in range(self.grid_size):
                val = board[r][col]
                if val == 0: continue
                board[r][col] = 0
                if not self.is_valid(board, r, col, val):
                    self.cells[r][col].config(bg=c["err"])
                board[r][col] = val

    def update_live_progress_bar(self):
        total_slots = self.grid_size * self.grid_size
        filled = sum(1 for r in range(self.grid_size) for c in range(self.grid_size) if self.cells[r][c].get() != "")
        pixel_width = int((filled / total_slots) * 240)
        self.ui_progress_bar.coords(self.ui_progress_fill, 0, 0, pixel_width, 8)

    def purchase_smart_hint(self):
        if self.total_points < 100:
            messagebox.showwarning("No Points", "Insufficient points available to buy a hint!")
            return
        board = self.get_matrix_from_gui()
        solution = [row[:] for row in board]
        if not self.solve_core(solution):
            messagebox.showerror("Error", "Fix active red error blocks before using a hint.")
            return
        empty_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if board[r][c] == 0]
        if not empty_cells: return
        r, c = random.choice(empty_cells)
        val = solution[r][c]
        self.cells[r][c].insert(0, str(val))
        self.cells[r][c].config(fg="#FFD700" if self.current_theme != "white" else "#D9A700", bg=self.get_colors()["sub"])
        self.total_points -= 100
        self.save_profile_to_disk()
        self.update_live_progress_bar()
        self.check_realtime_conflicts()

    def trigger_tachyon_flash(self):
        board = self.get_matrix_from_gui()
        solution = [row[:] for row in board]
        if not self.solve_core(solution): return
        empty_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if board[r][c] == 0]
        if not empty_cells: return
        targets = random.sample(empty_cells, min(2, len(empty_cells)))
        for r, c in targets:
            self.cells[r][c].insert(0, str(solution[r][c]))
            self.cells[r][c].config(fg="#FFD700" if self.current_theme != "white" else "#D9A700", bg="#3A0D23" if self.current_theme != "white" else "#E5E5EA")
        def clear_flash():
            for r, c in targets:
                if board[r][c] == 0: 
                    self.cells[r][c].delete(0, tk.END)
                    self.cells[r][c].config(fg=self.get_colors()["fg"], bg=self.get_colors()["cell_bg"])
            self.check_realtime_conflicts()
        self.root.after(1200, clear_flash)

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.auto_solved = False
        self.update_timer_loop()

    def update_timer_loop(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed, 60)
            self.timer_label.config(text=f"TIME: {mins:02d}:{secs:02d}")
            self.root.after(1000, self.update_timer_loop)

    def clear_grid(self):
        c = self.get_colors()
        for r in range(self.grid_size):
            for col in range(self.grid_size):
                self.cells[r][col].delete(0, tk.END)
                self.cells[r][col].config(fg=c["fg"], bg=c["cell_bg"])
        self.auto_solved = False
        self.update_live_progress_bar()

    def get_matrix_from_gui(self):
        matrix = []
        for r in range(self.grid_size):
            row = []
            for col in range(self.grid_size):
                val = self.cells[r][col].get()
                row.append(int(val) if val != "" else 0)
            matrix.append(row)
        return matrix

    def is_valid(self, board, row, col, num):
        if num in board[row]: return False
        if num in [board[i][col] for i in range(self.grid_size)]: return False
        box_rows, box_cols = self.get_subgrid_dims()
        bx, by = (col // box_cols) * box_cols, (row // box_rows) * box_rows
        for i in range(by, by + box_rows):
            for j in range(bx, bx + box_cols):
                if board[i][j] == num: return False
        return True

    def solve_core(self, board):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if board[r][c] == 0:
                    for num in range(1, self.grid_size + 1):
                        if self.is_valid(board, r, c, num):
                            board[r][c] = num
                            if self.solve_core(board): return True
                            board[r][c] = 0
                    return False
        return True

    def inject_random_generated_game(self):
        self.clear_grid()
        base = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.solve_core(base)
        quota = 5 if self.grid_size == 4 else (12 if self.grid_size == 6 else 26)
        while quota > 0:
            r, col = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if base[r][col] != 0:
                base[r][col] = 0
                quota -= 1
        for r in range(self.grid_size):
            for col in range(self.grid_size):
                if base[r][col] != 0:
                    self.cells[r][col].insert(0, str(base[r][col]))
        self.start_timer()
        self.update_live_progress_bar()

    def inject_daily_challenge_blueprint(self):
        self.clear_grid()
        day_seed = int(time.strftime("%Y%m%d"))
        random.seed(day_seed)
        base = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.solve_core(base)
        quota = 6 if self.grid_size == 4 else 18
        while quota > 0:
            r, col = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if base[r][col] != 0:
                base[r][col] = 0
                quota -= 1
        for r in range(self.grid_size):
            for col in range(self.grid_size):
                if base[r][col] != 0:
                    self.cells[r][col].insert(0, str(base[r][col]))
                    self.cells[r][col].config(fg=self.get_colors()["grid_line"])
        random.seed()
        self.update_live_progress_bar()

    def trigger_solver(self):
        self.timer_running = False
        self.auto_solved = True 
        board = self.get_matrix_from_gui()
        c = self.get_colors()
        solution = [row[:] for row in board]
        if not self.solve_core(solution):
            messagebox.showerror("Error", "No valid board solution found.")
            return
        for r in range(self.grid_size):
            for col in range(self.grid_size):
                if board[r][col] == 0:
                    self.cells[r][col].insert(0, str(solution[r][col]))
                    self.cells[r][col].config(fg=c["grid_line"])
        self.update_live_progress_bar()

    def evaluate_user_game(self):
        if not self.timer_running: return 
        self.timer_running = False
        
        user_board = self.get_matrix_from_gui()
        elapsed = int(time.time() - self.start_time)
        mins, secs = divmod(elapsed, 60)
        time_str = f"{mins:02d}:{secs:02d}"

        is_perfect = True
        for r in range(self.grid_size):
            for col in range(self.grid_size):
                val = user_board[r][col]
                if val == 0: is_perfect = False; break
                user_board[r][col] = 0
                if not self.is_valid(user_board, r, col, val): is_perfect = False
                user_board[r][col] = val
        
        if is_perfect and not self.auto_solved:
            base_reward = 300 if self.grid_size == 4 else (600 if self.grid_size == 6 else 1000)
            score = max(150, base_reward - (elapsed * 2))
            self.solve_streak += 1
            self.total_points += score
        else:
            score = 0
            is_perfect = False
            
        self.session_history.append({
            "timestamp": time.strftime("%H:%M"),
            "size": f"{self.grid_size}x{self.grid_size}",
            "mode": "Daily" if self.is_daily_challenge else "Custom",
            "time": time_str,
            "accuracy": "WIN" if is_perfect else "LOSE",
            "score": score
        })
        self.save_profile_to_disk()
        
        self.show_victory_score_page(is_perfect, score, time_str)

    # --- VIEW 3: SCORE GAME OVER PAGE ---
    def show_victory_score_page(self, is_perfect, score, time_str):
        self.build_enclosed_canvas_box()
        c = self.get_colors()
        
        self.draw_global_exit_anchor(self.main_container)
        
        v_frame = tk.Frame(self.main_container, bg=c["bg"])
        v_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        if is_perfect:
            header_lbl = tk.Label(v_frame, text="✔ STAGE CLEAR!", font=("Courier New", 22, "bold"), fg="#00FF66" if self.current_theme != "white" else "#34C759", bg=c["bg"])
            header_lbl.pack(pady=15)
            sub_text = "ALL NUMBERS PLACED PERFECTLY"
        else:
            header_lbl = tk.Label(v_frame, text="✖ GAME OVER", font=("Courier New", 17, "bold"), fg="#FF1E56" if self.current_theme != "white" else "#FF3B30", bg=c["bg"])
            header_lbl.pack(pady=15)
            sub_text = "BOARD HAS DUPLICATE VALUES"
            
        tk.Label(v_frame, text=sub_text, font=("Courier New", 9), fg=c["fg"], bg=c["bg"]).pack()
        
        stat_box = tk.Frame(v_frame, bg=c["card"], padx=20, pady=20, highlightbackground=c["grid_line"], highlightthickness=1)
        stat_box.pack(fill="x", pady=20)
        
        tk.Label(stat_box, text=f"PLAYER NAME: {self.player_name.upper()}", font=("Courier New", 10, "bold"), fg=c["fg"], bg=c["card"]).pack(pady=5)
        tk.Label(stat_box, text=f"TIME ELAPSED: {time_str}", font=("Courier New", 10), fg=c["fg"], bg=c["card"]).pack(pady=5)
        
        score_lbl = tk.Label(stat_box, text=f"EARNED HIGH SCORE: +0 PTS", font=("Courier New", 11, "bold"), fg=c["accent"], bg=c["card"])
        score_lbl.pack(pady=10)
        
        streak_lbl = tk.Label(v_frame, text=f"🔥 WIN STREAK: {self.solve_streak} DAYS", font=("Courier New", 11, "bold"), fg="#FFD700" if self.current_theme != "white" else "#D9A700", bg=c["bg"])
        streak_lbl.pack(pady=10)

        def tally_points_animation(current=0):
            if current <= score:
                score_lbl.config(text=f"EARNED HIGH SCORE: +{current} PTS")
                self.root.after(10, lambda: tally_points_animation(current + max(1, score//25)))
            else:
                score_lbl.config(text=f"EARNED HIGH SCORE: +{score} PTS")
                streak_lbl.config(fg=c["accent"])
                self.root.after(200, lambda: streak_lbl.config(fg="#FFD700" if self.current_theme != "white" else "#D9A700"))
                
        if score > 0:
            self.root.after(400, lambda: tally_points_animation(0))
        else:
            score_lbl.config(text="EARNED HIGH SCORE: 0 PTS", fg="#555555")

        tk.Button(v_frame, text="RETURN TO MAIN MENU", font=("Courier New", 10, "bold"), bg=c["grid_line"] if self.current_theme != "white" else "#0088CC", fg="white", bd=0, padx=20, pady=8, command=self.show_title_screen).pack(pady=20)

    # --- VIEW 4: PERFORMANCE STATS DASHBOARD ---
    def show_dashboard_screen(self):
        self.build_enclosed_canvas_box()
        c = self.get_colors()
        
        self.draw_global_exit_anchor(self.main_container)
        self.draw_status_ribbon(self.main_container)
        
        dash_card = tk.Frame(self.main_container, bg=c["card"], padx=15, pady=10, highlightbackground=c["grid_line"], highlightthickness=1)
        dash_card.pack(padx=15, pady=5, fill="both", expand=True)
        
        tk.Label(dash_card, text="⚡ PLAYER STATS & HIGHLIGHTS", font=("Courier New", 11, "bold"), fg=c["grid_line"] if self.current_theme != "white" else c["fg"], bg=c["card"]).pack(pady=4)
        
        badge_frame = tk.LabelFrame(dash_card, text=" UNLOCKED TROPHIES ", font=("Courier New", 8, "bold"), bg=c["card"], fg=c["grid_line"] if self.current_theme != "white" else c["fg"], bd=1)
        badge_frame.pack(fill="x", pady=4, ipady=2)
        
        badge_box = tk.Frame(badge_frame, bg=c["card"])
        badge_box.pack()
        
        badge_milestones = [("Beginner", 0), ("Pro Gamer", 400), ("Grandmaster", 1200)]
        for b_name, b_req in badge_milestones:
            unlocked = self.total_points >= b_req
            status = "🏆" if unlocked else "🔒"
            text_color = c["fg"] if unlocked else "#555555"
            tk.Label(badge_box, text=f"{status}{b_name}", font=("Courier New", 8, "bold"), fg=text_color, bg=c["sub"], padx=4, pady=2).pack(side="left", padx=4)

        graph_frame = tk.LabelFrame(dash_card, text=" SCORE GRADIENT HISTORY ", font=("Courier New", 8, "bold"), bg=c["card"], fg=c["grid_line"] if self.current_theme != "white" else c["fg"], bd=1)
        graph_frame.pack(fill="x", pady=4)
        
        graph_canvas = tk.Canvas(graph_frame, width=420, height=110, bg=c["cell_bg"], highlightthickness=0)
        graph_canvas.pack(pady=4, padx=4)
        
        scores = [log["score"] for log in self.session_history]
        if len(scores) >= 1:
            max_s = max(scores) if max(scores) > 0 else 100
            w_step = 360 / max(1, len(scores) - 1)
            for i, score in enumerate(scores):
                x = 25 + (i * w_step)
                y = 90 - (score / max_s * 65)
                if i > 0:
                    graph_canvas.create_line(prev_x, prev_y, x, y, fill=c["grid_line"], width=2)
                graph_canvas.create_oval(x-2, y-2, x+2, y+2, fill="#FFD700" if self.current_theme != "white" else "#D9A700")
                prev_x, prev_y = x, y
        else:
            graph_canvas.create_text(210, 55, text="AWAITING MATCH RECORD ENTRIES", fill="#555555", font=("Courier New", 8, "italic"))

        log_frame = tk.LabelFrame(dash_card, text=" RECENT MATCH RECORDS ", font=("Courier New", 8, "bold"), bg=c["card"], fg=c["grid_line"] if self.current_theme != "white" else c["fg"], bd=1)
        log_frame.pack(fill="both", expand=True, pady=4)
        
        for log in self.session_history[-4:]: 
            tk.Label(log_frame, text=f"⏱️ {log['size']} | {log['mode']} | Pts: {log['score']} | {log['accuracy']}", font=("Courier New", 8), fg=c["fg"], bg=c["card"]).pack(anchor="w", padx=8, pady=1)

        tk.Button(dash_card, text="← RESUME PUZZLE GAME", font=("Courier New", 9, "bold"), bg=c["sub"], fg=c["fg"], bd=1, pady=4, command=self.show_game_screen).pack(fill="x", pady=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuQuantumPro(root)
    root.mainloop()