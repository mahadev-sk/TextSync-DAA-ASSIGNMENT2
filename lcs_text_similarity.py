"""
=============================================================================
  LCS Text Similarity Checker
  Algorithm: Longest Common Subsequence (Dynamic Programming)
  
  A GUI application that computes the LCS of two strings, visualizes the
  DP table step-by-step, highlights the matching subsequence, and reports
  a similarity percentage.
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time

# ═══════════════════════════════════════════════════════════════════════════
#  CORE ALGORITHM
# ═══════════════════════════════════════════════════════════════════════════

def compute_lcs(text1, text2):
    """
    Compute the Longest Common Subsequence using bottom-up Dynamic Programming.

    Time Complexity  : O(m * n)
    Space Complexity : O(m * n)
    where m = len(text1), n = len(text2)

    Returns:
        dp    – the complete DP table (list of lists)
        lcs   – the LCS string itself
        steps – list of (i, j, value, is_match) for animation
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    steps = []  # records every cell fill for animation

    # ── Fill DP table ──
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                steps.append((i, j, dp[i][j], True))   # match
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                steps.append((i, j, dp[i][j], False))  # no match

    # ── Backtrack to find the actual LCS string ──
    lcs_chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs_chars.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    lcs = "".join(reversed(lcs_chars))

    return dp, lcs, steps


def get_lcs_indices(text, lcs_str):
    """Return the indices in *text* that form the LCS, greedily matched."""
    indices = []
    li = 0
    for ti, ch in enumerate(text):
        if li < len(lcs_str) and ch == lcs_str[li]:
            indices.append(ti)
            li += 1
    return indices


# ═══════════════════════════════════════════════════════════════════════════
#  GUI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

class LCSApp:
    # ── colour palette ──
    BG           = "#1e1e2e"
    FG           = "#cdd6f4"
    ACCENT       = "#89b4fa"
    MATCH_CLR    = "#a6e3a1"
    NO_MATCH_CLR = "#f38ba8"
    HEADER_CLR   = "#b4befe"
    CELL_BG      = "#313244"
    BTN_BG       = "#45475a"
    HIGHLIGHT    = "#f9e2af"

    def __init__(self, root):
        self.root = root
        self.root.title("LCS Text Similarity Checker — Dynamic Programming")
        self.root.configure(bg=self.BG)
        self.root.geometry("1050x750")
        self.root.minsize(900, 650)

        self.animating = False
        self.anim_speed = 30        # ms per cell
        self.current_step = 0
        self.steps = []
        self.dp = []
        self.text1 = ""
        self.text2 = ""
        self.cell_labels = {}

        self._build_ui()

    # ─────────────────────── UI CONSTRUCTION ───────────────────────

    def _build_ui(self):
        # ── Title ──
        title = tk.Label(
            self.root, text="📝  LCS Text Similarity Checker",
            font=("Segoe UI", 18, "bold"), bg=self.BG, fg=self.ACCENT
        )
        title.pack(pady=(12, 4))

        subtitle = tk.Label(
            self.root,
            text="Algorithm: Longest Common Subsequence  •  Technique: Dynamic Programming",
            font=("Segoe UI", 10), bg=self.BG, fg="#7f849c"
        )
        subtitle.pack()

        # ── Input frame ──
        inp_frame = tk.Frame(self.root, bg=self.BG)
        inp_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(inp_frame, text="Text 1:", font=("Segoe UI", 11, "bold"),
                 bg=self.BG, fg=self.FG).grid(row=0, column=0, sticky="w")
        self.entry1 = tk.Entry(inp_frame, font=("Consolas", 12), width=40,
                               bg=self.CELL_BG, fg=self.FG, insertbackground=self.FG,
                               relief="flat", bd=4)
        self.entry1.grid(row=0, column=1, padx=8, pady=4, sticky="ew")
        self.entry1.insert(0, "ALGORITHM")

        tk.Label(inp_frame, text="Text 2:", font=("Segoe UI", 11, "bold"),
                 bg=self.BG, fg=self.FG).grid(row=1, column=0, sticky="w")
        self.entry2 = tk.Entry(inp_frame, font=("Consolas", 12), width=40,
                               bg=self.CELL_BG, fg=self.FG, insertbackground=self.FG,
                               relief="flat", bd=4)
        self.entry2.grid(row=1, column=1, padx=8, pady=4, sticky="ew")
        self.entry2.insert(0, "ALTRUISTIC")

        inp_frame.columnconfigure(1, weight=1)

        # ── Buttons ──
        btn_frame = tk.Frame(self.root, bg=self.BG)
        btn_frame.pack(pady=6)

        self.btn_compute = tk.Button(
            btn_frame, text="▶  Compute LCS", font=("Segoe UI", 11, "bold"),
            bg=self.ACCENT, fg="#1e1e2e", activebackground="#74c7ec",
            relief="flat", padx=16, pady=4, command=self.on_compute
        )
        self.btn_compute.grid(row=0, column=0, padx=6)

        self.btn_animate = tk.Button(
            btn_frame, text="⏩  Animate", font=("Segoe UI", 11, "bold"),
            bg="#a6e3a1", fg="#1e1e2e", activebackground="#94e2d5",
            relief="flat", padx=16, pady=4, command=self.on_animate
        )
        self.btn_animate.grid(row=0, column=1, padx=6)

        self.btn_clear = tk.Button(
            btn_frame, text="🗑  Clear", font=("Segoe UI", 11),
            bg=self.BTN_BG, fg=self.FG, activebackground="#585b70",
            relief="flat", padx=16, pady=4, command=self.on_clear
        )
        self.btn_clear.grid(row=0, column=2, padx=6)

        # speed slider
        tk.Label(btn_frame, text="Speed:", font=("Segoe UI", 9),
                 bg=self.BG, fg="#7f849c").grid(row=0, column=3, padx=(16, 2))
        self.speed_var = tk.IntVar(value=30)
        self.speed_slider = tk.Scale(
            btn_frame, from_=5, to=200, orient="horizontal", length=120,
            variable=self.speed_var, bg=self.BG, fg=self.FG,
            troughcolor=self.CELL_BG, highlightthickness=0,
            command=lambda v: setattr(self, 'anim_speed', int(v))
        )
        self.speed_slider.grid(row=0, column=4)
        tk.Label(btn_frame, text="ms", font=("Segoe UI", 9),
                 bg=self.BG, fg="#7f849c").grid(row=0, column=5)

        # ── Results bar ──
        self.result_frame = tk.Frame(self.root, bg=self.BG)
        self.result_frame.pack(fill="x", padx=20)

        self.lbl_lcs = tk.Label(
            self.result_frame, text="LCS: —", font=("Consolas", 12, "bold"),
            bg=self.BG, fg=self.HIGHLIGHT, anchor="w"
        )
        self.lbl_lcs.pack(side="left", padx=(0, 20))

        self.lbl_len = tk.Label(
            self.result_frame, text="Length: —", font=("Segoe UI", 11),
            bg=self.BG, fg=self.FG, anchor="w"
        )
        self.lbl_len.pack(side="left", padx=(0, 20))

        self.lbl_sim = tk.Label(
            self.result_frame, text="Similarity: —", font=("Segoe UI", 11, "bold"),
            bg=self.BG, fg=self.MATCH_CLR, anchor="w"
        )
        self.lbl_sim.pack(side="left")

        # ── Highlighted input display ──
        self.highlight_frame = tk.Frame(self.root, bg=self.BG)
        self.highlight_frame.pack(fill="x", padx=20, pady=(6, 2))

        tk.Label(self.highlight_frame, text="Text 1:", font=("Segoe UI", 10),
                 bg=self.BG, fg="#7f849c").grid(row=0, column=0, sticky="w")
        self.hl_text1 = tk.Text(
            self.highlight_frame, height=1, font=("Consolas", 13),
            bg=self.CELL_BG, fg=self.FG, relief="flat", bd=4, wrap="none"
        )
        self.hl_text1.grid(row=0, column=1, sticky="ew", padx=6, pady=2)
        self.hl_text1.tag_configure("match", foreground="#1e1e2e", background=self.MATCH_CLR,
                                    font=("Consolas", 13, "bold"))

        tk.Label(self.highlight_frame, text="Text 2:", font=("Segoe UI", 10),
                 bg=self.BG, fg="#7f849c").grid(row=1, column=0, sticky="w")
        self.hl_text2 = tk.Text(
            self.highlight_frame, height=1, font=("Consolas", 13),
            bg=self.CELL_BG, fg=self.FG, relief="flat", bd=4, wrap="none"
        )
        self.hl_text2.grid(row=1, column=1, sticky="ew", padx=6, pady=2)
        self.hl_text2.tag_configure("match", foreground="#1e1e2e", background=self.MATCH_CLR,
                                    font=("Consolas", 13, "bold"))

        self.highlight_frame.columnconfigure(1, weight=1)

        # ── DP Table (scrollable) ──
        table_outer = tk.Frame(self.root, bg=self.BG)
        table_outer.pack(fill="both", expand=True, padx=20, pady=(6, 12))

        self.table_canvas = tk.Canvas(table_outer, bg=self.BG, highlightthickness=0)
        vsb = ttk.Scrollbar(table_outer, orient="vertical", command=self.table_canvas.yview)
        hsb = ttk.Scrollbar(table_outer, orient="horizontal", command=self.table_canvas.xview)
        self.table_canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.table_canvas.pack(side="left", fill="both", expand=True)

        self.table_frame = tk.Frame(self.table_canvas, bg=self.BG)
        self.table_canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        self.table_frame.bind("<Configure>",
                              lambda e: self.table_canvas.configure(
                                  scrollregion=self.table_canvas.bbox("all")))

    # ─────────────────────── ACTIONS ───────────────────────

    def on_clear(self):
        self.animating = False
        self.entry1.delete(0, "end")
        self.entry2.delete(0, "end")
        self.lbl_lcs.config(text="LCS: —")
        self.lbl_len.config(text="Length: —")
        self.lbl_sim.config(text="Similarity: —")
        self._clear_table()
        self._clear_highlights()

    def _clear_table(self):
        for w in self.table_frame.winfo_children():
            w.destroy()
        self.cell_labels = {}

    def _clear_highlights(self):
        self.hl_text1.config(state="normal")
        self.hl_text1.delete("1.0", "end")
        self.hl_text1.config(state="disabled")
        self.hl_text2.config(state="normal")
        self.hl_text2.delete("1.0", "end")
        self.hl_text2.config(state="disabled")

    # ── Compute (instant) ──

    def on_compute(self):
        self.animating = False
        t1 = self.entry1.get().strip()
        t2 = self.entry2.get().strip()
        if not t1 or not t2:
            messagebox.showwarning("Input required", "Please enter both texts.")
            return
        if len(t1) > 30 or len(t2) > 30:
            messagebox.showwarning("Too long",
                                   "Please keep both strings ≤ 30 characters for clear display.")
            return

        self.text1, self.text2 = t1, t2
        self.dp, lcs, self.steps = compute_lcs(t1, t2)
        self._draw_table_full(t1, t2, self.dp)
        self._show_results(t1, t2, lcs)

    # ── Animate (step-by-step) ──

    def on_animate(self):
        t1 = self.entry1.get().strip()
        t2 = self.entry2.get().strip()
        if not t1 or not t2:
            messagebox.showwarning("Input required", "Please enter both texts.")
            return
        if len(t1) > 30 or len(t2) > 30:
            messagebox.showwarning("Too long",
                                   "Please keep both strings ≤ 30 characters for clear display.")
            return

        self.animating = True
        self.text1, self.text2 = t1, t2
        self.dp, lcs, self.steps = compute_lcs(t1, t2)
        self.current_step = 0

        # draw empty grid
        self._draw_table_empty(t1, t2)
        self._animate_next(t1, t2, lcs)

    def _animate_next(self, t1, t2, lcs):
        if not self.animating:
            return
        if self.current_step >= len(self.steps):
            # animation done — show final colours & results
            self._colour_backtrack(t1, t2)
            self._show_results(t1, t2, lcs)
            self.animating = False
            return

        i, j, val, is_match = self.steps[self.current_step]
        lbl = self.cell_labels.get((i, j))
        if lbl:
            lbl.config(text=str(val),
                       bg=self.MATCH_CLR if is_match else self.NO_MATCH_CLR,
                       fg="#1e1e2e")
        self.current_step += 1
        self.root.after(self.anim_speed, self._animate_next, t1, t2, lcs)

    # ─────────────────────── TABLE DRAWING ───────────────────────

    def _make_header(self, parent, text, row, col):
        lbl = tk.Label(parent, text=text, width=4, height=1,
                       font=("Consolas", 11, "bold"),
                       bg=self.HEADER_CLR, fg="#1e1e2e", relief="ridge", bd=1)
        lbl.grid(row=row, column=col, padx=1, pady=1)
        return lbl

    def _draw_table_empty(self, t1, t2):
        """Draw the DP grid with headers and zero-initialised first row/col."""
        self._clear_table()
        m, n = len(t1), len(t2)

        # corner
        self._make_header(self.table_frame, "", 0, 0)
        self._make_header(self.table_frame, "ε", 0, 1)
        for j, ch in enumerate(t2):
            self._make_header(self.table_frame, ch, 0, j + 2)

        self._make_header(self.table_frame, "ε", 1, 0)
        for i, ch in enumerate(t1):
            self._make_header(self.table_frame, ch, i + 2, 0)

        # fill zeros for row-0 and col-0
        for j in range(n + 1):
            lbl = tk.Label(self.table_frame, text="0", width=4, height=1,
                           font=("Consolas", 11), bg=self.CELL_BG, fg=self.FG,
                           relief="ridge", bd=1)
            lbl.grid(row=1, column=j + 1, padx=1, pady=1)
            self.cell_labels[(0, j)] = lbl

        for i in range(1, m + 1):
            lbl = tk.Label(self.table_frame, text="0", width=4, height=1,
                           font=("Consolas", 11), bg=self.CELL_BG, fg=self.FG,
                           relief="ridge", bd=1)
            lbl.grid(row=i + 1, column=1, padx=1, pady=1)
            self.cell_labels[(i, 0)] = lbl

        # inner cells — blank
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                lbl = tk.Label(self.table_frame, text="", width=4, height=1,
                               font=("Consolas", 11), bg=self.CELL_BG, fg=self.FG,
                               relief="ridge", bd=1)
                lbl.grid(row=i + 1, column=j + 1, padx=1, pady=1)
                self.cell_labels[(i, j)] = lbl

    def _draw_table_full(self, t1, t2, dp):
        """Draw the completed DP table at once (used by instant compute)."""
        self._draw_table_empty(t1, t2)
        m, n = len(t1), len(t2)
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                is_match = t1[i - 1] == t2[j - 1]
                lbl = self.cell_labels[(i, j)]
                lbl.config(
                    text=str(dp[i][j]),
                    bg=self.MATCH_CLR if is_match else self.CELL_BG,
                    fg="#1e1e2e" if is_match else self.FG
                )
        self._colour_backtrack(t1, t2)

    def _colour_backtrack(self, t1, t2):
        """Highlight backtrack path cells with gold."""
        m, n = len(t1), len(t2)
        i, j = m, n
        while i > 0 and j > 0:
            lbl = self.cell_labels.get((i, j))
            if t1[i - 1] == t2[j - 1]:
                if lbl:
                    lbl.config(bg=self.HIGHLIGHT, fg="#1e1e2e",
                               font=("Consolas", 11, "bold"))
                i -= 1
                j -= 1
            elif self.dp[i - 1][j] > self.dp[i][j - 1]:
                i -= 1
            else:
                j -= 1

    # ─────────────────────── RESULTS DISPLAY ───────────────────────

    def _show_results(self, t1, t2, lcs):
        lcs_len = len(lcs)
        max_len = max(len(t1), len(t2))
        similarity = (lcs_len / max_len * 100) if max_len else 0

        self.lbl_lcs.config(text=f"LCS: \"{lcs}\"")
        self.lbl_len.config(text=f"Length: {lcs_len}")
        self.lbl_sim.config(text=f"Similarity: {similarity:.1f}%")

        # highlight matching chars in both texts
        idx1 = get_lcs_indices(t1, lcs)
        idx2 = get_lcs_indices(t2, lcs)

        self.hl_text1.config(state="normal")
        self.hl_text1.delete("1.0", "end")
        for i, ch in enumerate(t1):
            tag = "match" if i in idx1 else ""
            self.hl_text1.insert("end", ch, tag)
        self.hl_text1.config(state="disabled")

        self.hl_text2.config(state="normal")
        self.hl_text2.delete("1.0", "end")
        for i, ch in enumerate(t2):
            tag = "match" if i in idx2 else ""
            self.hl_text2.insert("end", ch, tag)
        self.hl_text2.config(state="disabled")


# ═══════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = LCSApp(root)
    root.mainloop()
