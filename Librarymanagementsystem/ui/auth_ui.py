import tkinter as tk
from tkinter import messagebox
import json
import os

class AuthUI(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.mode = "login"  # login | register

        # Đọc đúng file data/user.json của nhóm
        self.users_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),  # Librarymanagementsystem/
            "data",
            "users.json"
        )

        self.build_ui()

    # ===== JSON Helpers =====
    def load_users(self):
        if not os.path.exists(self.users_file):
            print(f"Không tìm thấy file: {self.users_file}")
            return []

        try:
            with open(self.users_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("File users.json bị lỗi định dạng JSON.")
            return []
        except Exception as e:
            print(f"Lỗi khi đọc file users.json: {e}")
            return []

    def save_users(self, users):
        try:
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            with open(self.users_file, "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi lưu file: {e}")
            return False

    def user_exists(self, username):
        users = self.load_users()
        return any(u.get("username") == username for u in users)

    def register_user(self, username, password):
        users = self.load_users()

        if self.user_exists(username):
            return False, "Username đã tồn tại."

        if len(password) < 8:
            return False, "Mật khẩu phải có ít nhất 8 ký tự."

        # Tạo user_id mới
        new_id = max([u.get("user_id", 0) for u in users], default=0) + 1

        new_user = {
            "user_id": new_id,
            "username": username,
            "email": f"{username}@example.com",
            "password": password,
            "full_name": username.title(),
            "phone_number": "0123456789",
            "status": "ACTIVE",
            "role": "MEMBER",
            "borrowing_limit": 5,
            "penalty_status": False,
            "created_at": "2026-01-25T00:00:00"
        }

        users.append(new_user)
        if self.save_users(users):
            return True, "Đăng ký thành công!"
        else:
            return False, "Lỗi khi lưu thông tin."

    def login_user(self, username, password):
        users = self.load_users()

        for u in users:
            if u.get("username") == username and u.get("password") == password:
                if u.get("status") != "ACTIVE":
                    return False, f"Tài khoản bị {u.get('status', 'khóa')}."
                return True, f"Xin chào {u.get('full_name', username)}!"
        return False, "Sai username hoặc password."

    # ===== UI =====
    def build_ui(self):
        self.configure(bg="white")
        
        # Title
        self.title_label = tk.Label(
            self, 
            text="ĐĂNG NHẬP HỆ THỐNG", 
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        self.title_label.pack(pady=30)

        # Form container
        form_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        form_frame.pack()

        # Username
        tk.Label(
            form_frame, 
            text="Username:", 
            font=("Arial", 11),
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=8)
        
        self.username_entry = tk.Entry(
            form_frame, 
            width=30,
            font=("Arial", 11),
            relief="solid"
        )
        self.username_entry.grid(row=0, column=1, pady=8, padx=(10, 0))

        # Password
        tk.Label(
            form_frame, 
            text="Password:", 
            font=("Arial", 11),
            bg="white"
        ).grid(row=1, column=0, sticky="w", pady=8)
        
        self.password_entry = tk.Entry(
            form_frame, 
            width=30,
            font=("Arial", 11),
            show="*",
            relief="solid"
        )
        self.password_entry.grid(row=1, column=1, pady=8, padx=(10, 0))

        # Confirm Password (hidden by default)
        self.confirm_label = tk.Label(
            form_frame, 
            text="Confirm:", 
            font=("Arial", 11),
            bg="white"
        )
        self.confirm_entry = tk.Entry(
            form_frame, 
            width=30,
            font=("Arial", 11),
            show="*",
            relief="solid"
        )

        # Action button
        self.action_btn = tk.Button(
            self,
            text="ĐĂNG NHẬP",
            width=20,
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            relief="raised",
            padx=10,
            pady=5,
            command=self.handle_action
        )
        self.action_btn.pack(pady=15)

        # Switch mode button
        self.switch_btn = tk.Button(
            self,
            text="Chưa có tài khoản? Đăng ký",
            font=("Arial", 9),
            bg="white",
            fg="#2980b9",
            relief="flat",
            command=self.switch_mode
        )
        self.switch_btn.pack(pady=5)

        # Info label
        self.info = tk.Label(
            self, 
            text="",
            font=("Arial", 9),
            bg="white",
            fg="#27ae60"
        )
        self.info.pack(pady=10)

        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.handle_action())
        self.password_entry.bind("<Return>", lambda e: self.handle_action())
        self.confirm_entry.bind("<Return>", lambda e: self.handle_action())

    def switch_mode(self):
        if self.mode == "login":
            self.mode = "register"
            self.title_label.config(text="ĐĂNG KÝ TÀI KHOẢN")
            self.action_btn.config(text="ĐĂNG KÝ", bg="#2ecc71")
            self.switch_btn.config(text="Đã có tài khoản? Đăng nhập")

            # Show confirm fields
            self.confirm_label.grid(row=2, column=0, sticky="w", pady=8)
            self.confirm_entry.grid(row=2, column=1, pady=8, padx=(10, 0))
        else:
            self.mode = "login"
            self.title_label.config(text="ĐĂNG NHẬP HỆ THỐNG")
            self.action_btn.config(text="ĐĂNG NHẬP", bg="#3498db")
            self.switch_btn.config(text="Chưa có tài khoản? Đăng ký")

            # Hide confirm fields
            self.confirm_label.grid_forget()
            self.confirm_entry.grid_forget()

        # Clear fields
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_entry.delete(0, tk.END)
        self.info.config(text="")
        self.username_entry.focus()

    def handle_action(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ username và password.")
            return

        # ===== REGISTER =====
        if self.mode == "register":
            confirm = self.confirm_entry.get().strip()

            if not confirm:
                messagebox.showwarning("Thông báo", "Vui lòng nhập Confirm Password.")
                return

            if password != confirm:
                messagebox.showwarning("Thông báo", "Password và Confirm Password không khớp.")
                return

            if len(username) < 3:
                messagebox.showwarning("Thông báo", "Username phải có ít nhất 3 ký tự.")
                return

            ok, msg = self.register_user(username, password)
            if ok:
                messagebox.showinfo("Thành công", msg)
                self.switch_mode()  # Switch back to login
            else:
                messagebox.showerror("Lỗi", msg)
            return

        # ===== LOGIN =====
        ok, msg = self.login_user(username, password)
        if ok:
            self.info.config(text=msg)
            
            # Delay a bit before switching
            self.after(500, lambda: self.app.show("main"))
        else:
            messagebox.showerror("Lỗi đăng nhập", msg)
            self.info.config(text=msg)