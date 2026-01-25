class AdminUI:
    def __init__(self):
        pass

    def admin_menu(self):
        print("\n========== ADMIN MENU ==========")
        print("1. Thêm sách")
        print("2. Xóa sách")
        print("3. Quay lại")

class AdminUI(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        tk.Button(
            self,
            text="⬅ Quay lại",
            width=15,
            command=lambda: app.show("main")
        ).pack(anchor="w", padx=10, pady=5)
        self.app = app
        self.build_ui()

    def run(self):
        while True:
            self.admin_menu()
            choice = input("Chọn chức năng admin: ").strip()
            if choice == "1":
                isbn = input("ISBN: ").strip()
                title = input("Title: ").strip()
                print(f"✅ (Demo) Đã thêm sách: {isbn} - {title}")

            elif choice == "2":
                book_id = input("Book ID: ").strip()
                print(f"✅ (Demo) Đã xóa sách: {book_id}")

            elif choice == "3":
                break
            else:
                print("❌ Lựa chọn không hợp lệ.")
