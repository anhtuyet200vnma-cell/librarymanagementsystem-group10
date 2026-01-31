import tkinter as tk
from tkinter import Menu
from Librarymanagementsystem.ui.auth_ui import AuthUI
from Librarymanagementsystem.ui.main_ui import MainUI
from Librarymanagementsystem.ui.book_ui import BookUI
from Librarymanagementsystem.ui.borrow_ui import BorrowUI
from Librarymanagementsystem.ui.admin_ui import AdminUI


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")

        # ===== Khung chứa các màn hình =====
        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # ===== Tạo sẵn menu nhưng CHƯA hiện =====
        self.menubar = Menu(self)
        self.menubar.add_command(label="Trang chính", command=lambda: self.show("main"))
        self.menubar.add_command(label="Quản lý sách", command=lambda: self.show("books"))
        self.menubar.add_command(label="Mượn / Trả", command=lambda: self.show("borrow"))
        self.menubar.add_command(label="Quản trị", command=lambda: self.show("admin"))
        self.menubar.add_command(label="Đăng xuất", command=lambda: self.logout())

        # ===== Khởi tạo các màn hình =====
        self.frames = {}
        frames_list = [
            ("auth", AuthUI),
            ("main", MainUI),
            ("books", BookUI),
            ("borrow", BorrowUI),
            ("admin", AdminUI)
        ]

        for name, FrameClass in frames_list:
            self.frames[name] = FrameClass(container, self)
            self.frames[name].grid(row=0, column=0, sticky="nsew")

        # ===== Mặc định vào login -> menu ẨN =====
        self.hide_menu()
        self.show("auth")

    # ===== 2 hàm điều khiển menu =====
    def show_menu(self):
        self.config(menu=self.menubar)

    def hide_menu(self):
        self.config(menu="")

    # ===== Điều hướng =====
    def show(self, name):
        if name not in self.frames:
            print(f"[WARN] Không có màn hình: {name}")
            return

        # Nếu vào màn login -> ẩn menu
        if name == "auth":
            self.hide_menu()
        else:
            # Các màn còn lại là sau login -> hiện menu
            self.show_menu()

        self.frames[name].tkraise()
        self.update()

    # ===== Logout chuẩn =====
    def logout(self):
        self.hide_menu()
        self.show("auth")