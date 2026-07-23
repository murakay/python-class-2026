"""関数電卓 — Python 標準ライブラリ (tkinter + math) のみ使用"""

import math
import tkinter as tk


# ── カラーパレット ─────────────────────────────────────────────────────────────
BG       = "#1c1c1e"
DISP_BG  = "#1c1c1e"
HIST_BG  = "#111113"
BTN_NUM  = "#3a3a3c"
BTN_OP   = "#f09a36"
BTN_FN   = "#2c5f8a"
BTN_UTIL = "#555558"
BTN_MEM  = "#4a4a6a"
FG       = "#ffffff"
FG_DIM   = "#aaaaaa"


def _lighten(hex_color: str, amount: int = 30) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return "#{:02x}{:02x}{:02x}".format(
        min(255, r + amount), min(255, g + amount), min(255, b + amount)
    )


# ── ボタン定義 [label, row, col, colspan, color] ──────────────────────────────
LAYOUT = [
    # 関数行1
    ("sin",  0, 0, 1, BTN_FN),   ("cos",  0, 1, 1, BTN_FN),
    ("tan",  0, 2, 1, BTN_FN),   ("Deg",  0, 3, 1, BTN_UTIL),
    ("(",    0, 4, 1, BTN_UTIL),  (")",    0, 5, 1, BTN_UTIL),
    # 関数行2
    ("asin", 1, 0, 1, BTN_FN),   ("acos", 1, 1, 1, BTN_FN),
    ("atan", 1, 2, 1, BTN_FN),   ("x²",  1, 3, 1, BTN_FN),
    ("xʸ",  1, 4, 1, BTN_FN),   ("√",   1, 5, 1, BTN_FN),
    # 関数行3
    ("log",  2, 0, 1, BTN_FN),   ("ln",   2, 1, 1, BTN_FN),
    ("10ˣ", 2, 2, 1, BTN_FN),   ("eˣ",  2, 3, 1, BTN_FN),
    ("π",   2, 4, 1, BTN_FN),   ("e",    2, 5, 1, BTN_FN),
    # メモリ行
    ("MC",   3, 0, 1, BTN_MEM),  ("MR",   3, 1, 1, BTN_MEM),
    ("M+",   3, 2, 1, BTN_MEM),  ("M-",   3, 3, 1, BTN_MEM),
    ("⌫",   3, 4, 1, BTN_UTIL), ("C",    3, 5, 1, BTN_UTIL),
    # 数字・演算子
    ("7",    4, 0, 1, BTN_NUM),  ("8",    4, 1, 1, BTN_NUM),
    ("9",    4, 2, 1, BTN_NUM),  ("÷",   4, 3, 1, BTN_OP),
    ("+/-",  4, 4, 1, BTN_UTIL), ("%",    4, 5, 1, BTN_UTIL),
    ("4",    5, 0, 1, BTN_NUM),  ("5",    5, 1, 1, BTN_NUM),
    ("6",    5, 2, 1, BTN_NUM),  ("×",   5, 3, 1, BTN_OP),
    ("1",    6, 0, 1, BTN_NUM),  ("2",    6, 1, 1, BTN_NUM),
    ("3",    6, 2, 1, BTN_NUM),  ("-",    6, 3, 1, BTN_OP),
    ("=",    6, 4, 2, BTN_OP),
    ("0",    7, 0, 2, BTN_NUM),  (".",    7, 2, 1, BTN_NUM),
    ("+",    7, 3, 1, BTN_OP),
]

KEY_MAP = {
    "Key-0":"0","Key-1":"1","Key-2":"2","Key-3":"3","Key-4":"4",
    "Key-5":"5","Key-6":"6","Key-7":"7","Key-8":"8","Key-9":"9",
    "period":".", "plus":"+", "minus":"-", "asterisk":"×", "slash":"÷",
    "parenleft":"(", "parenright":")",
    "Return":"=", "equal":"=",
    "BackSpace":"⌫", "Escape":"C",
    "percent":"%", "p":"π", "P":"π",
}


class FuncCalc:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("関数電卓")
        self.root.configure(bg=BG)
        self.root.minsize(560, 600)

        self.expr        = ""
        self.after_eq    = False   # = 直後フラグ
        self.deg_mode    = True
        self.memory      = 0.0

        self.var_expr    = tk.StringVar(value="")
        self.var_main    = tk.StringVar(value="0")
        self.var_mem     = tk.StringVar(value="")
        self.var_angle   = tk.StringVar(value="Deg")

        self._build_ui()
        self._bind_keys()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        left = tk.Frame(self.root, bg=BG)
        left.grid(row=0, column=0, sticky="nsew")

        right = tk.Frame(self.root, bg=HIST_BG, width=190)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_propagate(False)
        self._build_history(right)

        self._build_display(left)
        self._build_buttons(left)

    def _build_display(self, parent):
        f = tk.Frame(parent, bg=DISP_BG)
        f.grid(row=0, column=0, sticky="ew", padx=8, pady=(10, 2))
        f.columnconfigure(0, weight=1)

        info = tk.Frame(f, bg=DISP_BG)
        info.grid(row=0, column=0, sticky="ew")
        tk.Label(info, textvariable=self.var_mem,
                 bg=DISP_BG, fg=BTN_OP, font=("Helvetica", 10)
                 ).pack(side="left", padx=4)
        tk.Label(info, textvariable=self.var_angle,
                 bg=DISP_BG, fg="#5ac8fa", font=("Helvetica", 10)
                 ).pack(side="right", padx=6)

        tk.Label(f, textvariable=self.var_expr,
                 bg=DISP_BG, fg=FG_DIM, font=("Helvetica", 13),
                 anchor="e", justify="right"
                 ).grid(row=1, column=0, sticky="ew", padx=8)

        tk.Label(f, textvariable=self.var_main,
                 bg=DISP_BG, fg=FG, font=("Helvetica", 36, "bold"),
                 anchor="e", justify="right"
                 ).grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 6))

    def _build_buttons(self, parent):
        bf = tk.Frame(parent, bg=BG)
        bf.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))
        for c in range(6):
            bf.columnconfigure(c, weight=1)
        for r in range(8):
            bf.rowconfigure(r, weight=1)

        for label, row, col, cs, color in LAYOUT:
            hc = _lighten(color)
            btn = tk.Button(
                bf, text=label,
                font=("Helvetica", 13, "bold"),
                bg=color, fg=FG,
                activebackground=hc, activeforeground=FG,
                relief="flat", bd=0, cursor="hand2",
                command=lambda l=label: self._press(l),
            )
            btn.grid(row=row, column=col, columnspan=cs,
                     padx=2, pady=2, sticky="nsew", ipady=7)
            btn.bind("<Enter>", lambda e, b=btn, h=hc: b.config(bg=h))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

        parent.rowconfigure(0, weight=0)
        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)

    def _build_history(self, parent):
        tk.Label(parent, text="履歴", bg=HIST_BG, fg=FG_DIM,
                 font=("Helvetica", 11, "bold")).pack(pady=(8, 2))

        self.hist_lb = tk.Listbox(
            parent, bg=HIST_BG, fg=FG_DIM,
            selectbackground=BTN_FN,
            font=("Helvetica", 10),
            relief="flat", bd=0, activestyle="none",
        )
        self.hist_lb.pack(fill="both", expand=True, padx=4, pady=4)
        self.hist_lb.bind("<Double-Button-1>", self._recall)

        tk.Button(parent, text="クリア",
                  bg="#333335", fg=FG_DIM,
                  activebackground="#444446", activeforeground=FG,
                  relief="flat", bd=0, cursor="hand2",
                  command=lambda: self.hist_lb.delete(0, "end")
                  ).pack(fill="x", padx=4, pady=(0, 6))

    # ── キーバインド ──────────────────────────────────────────────────────────

    def _bind_keys(self):
        for key, label in KEY_MAP.items():
            self.root.bind(f"<{key}>", lambda e, l=label: self._press(l))

    # ── ボタン処理 ────────────────────────────────────────────────────────────

    def _press(self, label: str):
        try:
            self._handle(label)
        except Exception:
            self._error()

    def _handle(self, lbl: str):  # noqa: C901 (大きいが意図的に一か所に集約)
        # ──── ユーティリティ ────
        if lbl == "C":
            self.expr = ""
            self.after_eq = False
            self.var_expr.set("")
            self.var_main.set("0")
            return

        if lbl == "⌫":
            if self.after_eq:
                self.expr = ""
                self.after_eq = False
                self.var_main.set("0")
                self.var_expr.set("")
            else:
                self.expr = self.expr[:-1]
                self.var_main.set(self.expr or "0")
            return

        if lbl == "Deg":
            self.deg_mode = not self.deg_mode
            mode = "Deg" if self.deg_mode else "Rad"
            self.var_angle.set(mode)
            self.var_expr.set(f"[{mode}モード]")
            return

        # ──── メモリ ────
        if lbl == "MC":
            self.memory = 0.0
            self.var_mem.set("")
            return
        if lbl == "MR":
            self._insert(self._fmt(self.memory))
            return
        if lbl in ("M+", "M-"):
            v = self._eval(self.expr)
            if v is not None:
                self.memory += v if lbl == "M+" else -v
                self.var_mem.set(f"M={self._fmt(self.memory)}")
            return

        # ──── 符号反転 ────
        if lbl == "+/-":
            v = self._eval(self.expr)
            if v is not None:
                self.expr = self._fmt(-v)
                self.var_main.set(self.expr)
            return

        # ──── % ────
        if lbl == "%":
            v = self._eval(self.expr)
            if v is not None:
                self.expr = self._fmt(v / 100)
                self.var_main.set(self.expr)
            return

        # ──── = ────
        if lbl == "=":
            if not self.expr:
                return
            disp = self.expr
            v = self._eval(self.expr)
            if v is None:
                self._error()
                return
            rs = self._fmt(v)
            self.var_expr.set(disp + " =")
            self.var_main.set(rs)
            self._hist_add(f"{disp} = {rs}")
            self.expr = rs
            self.after_eq = True
            return

        # ──── 単項関数 (結果に直接適用) ────
        UNARY = {
            "sin":  (math.sin,  True,  True),   # (fn, use_deg_in, use_deg_out)
            "cos":  (math.cos,  True,  True),
            "tan":  (math.tan,  True,  True),
            "asin": (math.asin, False, True),
            "acos": (math.acos, False, True),
            "atan": (math.atan, False, True),
            "log":  (math.log10, False, False),
            "ln":   (math.log,   False, False),
            "x²":  (lambda x: x**2, False, False),
            "√":   (math.sqrt,   False, False),
            "10ˣ": (lambda x: 10**x, False, False),
            "eˣ":  (math.exp,    False, False),
        }
        if lbl in UNARY:
            fn, deg_in, deg_out = UNARY[lbl]
            if self.after_eq and self.expr:
                v = self._eval(self.expr)
                if v is None:
                    self._error(); return
                arg = math.radians(v) if (deg_in and self.deg_mode) else v
                res = fn(arg)
                if deg_out and self.deg_mode:
                    res = math.degrees(res)
                rs = self._fmt(res)
                self.var_expr.set(f"{lbl}({self._fmt(v)}) =")
                self.var_main.set(rs)
                self._hist_add(f"{lbl}({self._fmt(v)}) = {rs}")
                self.expr = rs
            else:
                # 関数名 + 開き括弧を式に追加
                fn_str = {
                    "sin":"sin(","cos":"cos(","tan":"tan(",
                    "asin":"asin(","acos":"acos(","atan":"atan(",
                    "log":"log10(","ln":"log(",
                    "x²":"(", "√":"sqrt(","10ˣ":"10**(","eˣ":"exp(",
                }[lbl]
                if self.after_eq:
                    self.expr = fn_str + self.expr
                    self.after_eq = False
                else:
                    self.expr += fn_str
                if lbl == "x²":
                    self.expr += ")**2"
                self.var_main.set(self.expr)
            return

        # ──── 定数 ────
        if lbl == "π":
            self._insert(str(math.pi))
            return
        if lbl == "e":
            self._insert(str(math.e))
            return

        # ──── べき乗 ────
        if lbl == "xʸ":
            self._insert("**")
            return

        # ──── 通常文字 (数字・演算子・括弧) ────
        c = {"×": "*", "÷": "/"}.get(lbl, lbl)
        if self.after_eq:
            if c in ("+", "-", "*", "/", "**"):
                self.expr += c
            else:
                self.expr = c
            self.after_eq = False
        else:
            self.expr += c
        self.var_main.set(self.expr)
        self.var_expr.set("")

    # ── 式の評価 ─────────────────────────────────────────────────────────────

    def _eval(self, expr: str) -> float | None:
        if not expr:
            return None
        try:
            deg = self.deg_mode
            def _r(x): return math.radians(x) if deg else x
            def _d(x): return math.degrees(x) if deg else x

            ns = {
                "sin":   lambda x: math.sin(_r(x)),
                "cos":   lambda x: math.cos(_r(x)),
                "tan":   lambda x: math.tan(_r(x)),
                "asin":  lambda x: _d(math.asin(x)),
                "acos":  lambda x: _d(math.acos(x)),
                "atan":  lambda x: _d(math.atan(x)),
                "log10": math.log10,
                "log":   math.log,
                "sqrt":  math.sqrt,
                "exp":   math.exp,
                "pi":    math.pi,
                "e":     math.e,
            }
            result = eval(expr, {"__builtins__": {}}, ns)  # noqa: S307
            return float(result)
        except Exception:
            return None

    # ── ヘルパー ──────────────────────────────────────────────────────────────

    def _insert(self, text: str):
        if self.after_eq:
            self.expr = text
            self.after_eq = False
        else:
            self.expr += text
        self.var_main.set(self.expr)

    def _error(self):
        self.var_main.set("エラー")
        self.var_expr.set("")
        self.expr = ""
        self.after_eq = False

    @staticmethod
    def _fmt(v: float) -> str:
        if math.isnan(v) or math.isinf(v):
            return "エラー"
        if v == int(v) and abs(v) < 1e15:
            return str(int(v))
        return f"{v:.10g}"

    def _hist_add(self, text: str):
        self.hist_lb.insert(0, text)
        if self.hist_lb.size() > 100:
            self.hist_lb.delete(100, "end")

    def _recall(self, _=None):
        sel = self.hist_lb.curselection()
        if not sel:
            return
        text = self.hist_lb.get(sel[0])
        if " = " in text:
            result = text.split(" = ")[-1]
            self.expr = result
            self.var_main.set(result)
            self.var_expr.set("")
            self.after_eq = True


# ── エントリーポイント ────────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    FuncCalc(root)
    root.mainloop()


if __name__ == "__main__":
    main()
