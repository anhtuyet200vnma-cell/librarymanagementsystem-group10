import tkinter as tk

class MainUI(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.build_ui()

    def build_ui(self):
        self.configure(bg="white")
        
        # Header
        tk.Label(
            self, 
            text="HỆ THỐNG QUẢN LÝ THƯ VIỆN", 
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=30)
        
        tk.Label(
            self,
            text="Chào mừng bạn đến với hệ thống",
            font=("Arial", 12),
            bg="white",
            fg="#7f8c8d"
        ).pack(pady=5)

        # Button container
        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(pady=30)

        # Buttons
        buttons = [
            ("📚 Quản lý sách", "books", "#1abc9c"),
            ("📖 Mượn / Trả sách", "borrow", "#3498db"),
            ("👨‍💼 Quản trị hệ thống", "admin", "#e74c3c"),
            ("🚪 Đăng xuất", "auth", "#95a5a6")
        ]

        for i, (text, screen, color) in enumerate(buttons):
            btn = tk.Button(
                button_frame,
                text=text,
                width=25,
                font=("Arial", 11, "bold"),
                bg=color,
                fg="white",
                relief="raised",
                padx=20,
                pady=10,
                command=lambda s=screen: self.app.show(s)
            )
            btn.grid(row=i, column=0, pady=8, padx=20)

        # Footer
        tk.Label(
            self,
            text="Library Management System © 2026",
            font=("Arial", 9),
            bg="white",
            fg="#bdc3c7"
        ).pack(side="bottom", pady=20)