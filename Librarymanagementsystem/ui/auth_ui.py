import tkinter as tk
from tkinter import messagebox


class AuthUI(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="ĐĂNG NHẬP", font=("Arial", 18, "bold")).pack(pady=15)

        box = tk.Frame(self)
        box.pack(pady=10)

        tk.Label(box, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(box, width=35)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(box, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(box, width=35, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        tk.Button(self, text="Login", width=20, command=self.handle_login).pack(pady=10)

        self.info = tk.Label(self, text="", fg="blue")
        self.info.pack(pady=5)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        ok, msg = self.app.controller.login(username, password)
        if ok:
            messagebox.showinfo("Login", msg)
            self.info.config(text=msg)
            self.app.show("books")
        else:
            messagebox.showerror("Login failed", msg)
            self.info.config(text=msg)