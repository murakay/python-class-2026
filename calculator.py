import tkinter as tk


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("計算機")
        self.root.resizable(False, False)

        self.expression = ""
        self.display_var = tk.StringVar(value="0")

        self._build_ui()

    def _build_ui(self):
        display = tk.Entry(
            self.root,
            textvariable=self.display_var,
            font=("Arial", 24),
            justify="right",
            bd=10,
            relief="flat",
            bg="#1e1e1e",
            fg="white",
            disabledforeground="white",
            disabledbackground="#1e1e1e",
            state="disabled",
            width=16,
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=8, pady=(12, 4))

        buttons = [
            ("C",    1, 0, "#555555", "white"),
            ("+/-",  1, 1, "#555555", "white"),
            ("%",    1, 2, "#555555", "white"),
            ("÷",    1, 3, "#f09a36", "white"),

            ("7",    2, 0, "#333333", "white"),
            ("8",    2, 1, "#333333", "white"),
            ("9",    2, 2, "#333333", "white"),
            ("×",    2, 3, "#f09a36", "white"),

            ("4",    3, 0, "#333333", "white"),
            ("5",    3, 1, "#333333", "white"),
            ("6",    3, 2, "#333333", "white"),
            ("-",    3, 3, "#f09a36", "white"),

            ("1",    4, 0, "#333333", "white"),
            ("2",    4, 1, "#333333", "white"),
            ("3",    4, 2, "#333333", "white"),
            ("+",    4, 3, "#f09a36", "white"),

            ("0",    5, 0, "#333333", "white"),   # spans 2 columns
            (".",    5, 2, "#333333", "white"),
            ("=",    5, 3, "#f09a36", "white"),
        ]

        for item in buttons:
            label, row, col, bg, fg = item
            colspan = 2 if label == "0" else 1
            btn = tk.Button(
                self.root,
                text=label,
                font=("Arial", 18, "bold"),
                bg=bg,
                fg=fg,
                activebackground="#888888" if bg == "#555555" else
                                "#ffbc5e" if bg == "#f09a36" else "#555555",
                activeforeground="white",
                relief="flat",
                bd=0,
                width=4 if colspan == 1 else 9,
                height=2,
                command=lambda l=label: self._on_button(l),
            )
            btn.grid(row=row, column=col, columnspan=colspan,
                     padx=4, pady=4, sticky="nsew")

        self.root.configure(bg="#1c1c1c")
        for i in range(6):
            self.root.rowconfigure(i, weight=1)
        for j in range(4):
            self.root.columnconfigure(j, weight=1)

    def _on_button(self, label):
        if label == "C":
            self.expression = ""
            self.display_var.set("0")

        elif label == "+/-":
            try:
                val = float(self.expression) * -1
                self.expression = str(int(val) if val == int(val) else val)
                self.display_var.set(self.expression)
            except (ValueError, ZeroDivisionError):
                pass

        elif label == "%":
            try:
                val = float(self.expression) / 100
                self.expression = str(int(val) if val == int(val) else val)
                self.display_var.set(self.expression)
            except (ValueError, ZeroDivisionError):
                pass

        elif label == "=":
            try:
                expr = self.expression.replace("×", "*").replace("÷", "/")
                result = eval(expr)  # noqa: S307 — input is built from button presses only
                result = int(result) if isinstance(result, float) and result == int(result) else result
                self.display_var.set(str(result))
                self.expression = str(result)
            except ZeroDivisionError:
                self.display_var.set("エラー")
                self.expression = ""
            except Exception:
                self.display_var.set("エラー")
                self.expression = ""

        else:
            if self.display_var.get() == "0" and label not in "+-×÷.":
                self.expression = label
            else:
                self.expression += label
            self.display_var.set(self.expression)


def main():
    root = tk.Tk()
    Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
