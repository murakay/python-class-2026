import json
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo_data.json")


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDoアプリ")
        self.root.geometry("420x480")
        self.root.configure(bg="#1c1c1c")
        self.root.resizable(False, False)

        self.tasks = self._load_tasks()

        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        input_frame = tk.Frame(self.root, bg="#1c1c1c")
        input_frame.pack(fill="x", padx=12, pady=12)

        self.entry_var = tk.StringVar()
        entry = tk.Entry(
            input_frame,
            textvariable=self.entry_var,
            font=("Arial", 14),
            bd=6,
            relief="flat",
            bg="#333333",
            fg="white",
            insertbackground="white",
        )
        entry.pack(side="left", fill="x", expand=True, ipady=4)
        entry.bind("<Return>", lambda event: self._add_task())

        add_btn = tk.Button(
            input_frame,
            text="追加",
            font=("Arial", 12, "bold"),
            bg="#f09a36",
            fg="white",
            activebackground="#ffbc5e",
            activeforeground="white",
            relief="flat",
            bd=0,
            command=self._add_task,
        )
        add_btn.pack(side="left", padx=(8, 0))

        list_frame = tk.Frame(self.root, bg="#1c1c1c")
        list_frame.pack(fill="both", expand=True, padx=12)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame,
            font=("Arial", 13),
            bg="#252525",
            fg="white",
            selectbackground="#f09a36",
            selectforeground="white",
            activestyle="none",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<Double-Button-1>", lambda event: self._toggle_done())
        scrollbar.config(command=self.listbox.yview)

        button_frame = tk.Frame(self.root, bg="#1c1c1c")
        button_frame.pack(fill="x", padx=12, pady=12)

        done_btn = tk.Button(
            button_frame,
            text="完了/未完了",
            font=("Arial", 11, "bold"),
            bg="#555555",
            fg="white",
            activebackground="#888888",
            activeforeground="white",
            relief="flat",
            bd=0,
            command=self._toggle_done,
        )
        done_btn.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 4))

        delete_btn = tk.Button(
            button_frame,
            text="削除",
            font=("Arial", 11, "bold"),
            bg="#c0392b",
            fg="white",
            activebackground="#e74c3c",
            activeforeground="white",
            relief="flat",
            bd=0,
            command=self._delete_task,
        )
        delete_btn.pack(side="left", fill="x", expand=True, ipady=4, padx=(4, 0))

    def _load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_tasks(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            prefix = "[済] " if task["done"] else "[  ] "
            self.listbox.insert(tk.END, prefix + task["title"])
            if task["done"]:
                self.listbox.itemconfig(tk.END, fg="#888888")

    def _add_task(self):
        title = self.entry_var.get().strip()
        if not title:
            return
        self.tasks.append({"title": title, "done": False})
        self.entry_var.set("")
        self._save_tasks()
        self._refresh_list()

    def _selected_index(self):
        selection = self.listbox.curselection()
        return selection[0] if selection else None

    def _toggle_done(self):
        index = self._selected_index()
        if index is None:
            return
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self._save_tasks()
        self._refresh_list()
        self.listbox.selection_set(index)

    def _delete_task(self):
        index = self._selected_index()
        if index is None:
            return
        if messagebox.askyesno("確認", f"「{self.tasks[index]['title']}」を削除しますか?"):
            del self.tasks[index]
            self._save_tasks()
            self._refresh_list()


def main():
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
