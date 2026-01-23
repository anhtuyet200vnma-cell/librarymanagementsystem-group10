"""
main_cli.py
Điểm khởi đầu cho giao diện dòng lệnh (CLI).
Chức năng: hiển thị menu chính và điều hướng các màn hình con.
"""

class MainCLI:
    def __init__(self):
        # Sau này có thể truyền SessionManager, services vào đây
        pass

    def show_menu(self):
        """Hiển thị menu chính"""
        print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
        print("1. Đăng nhập")
        print("2. Thoát")
        print("=============================================")

    def run(self):
        """Chạy vòng lặp chính của chương trình"""
        while True:
            self.show_menu()
            choice = input("Chọn chức năng: ").strip()

            if choice == "1":
                print("Bạn chọn: Đăng nhập")
                # TODO: Gọi Auth UI sau khi nhóm làm xong auth_ui.py
                print("(Chưa có auth_ui.py nên tạm thời chưa đăng nhập được)")
            
            elif choice == "2":
                print("Thoát chương trình. Tạm biệt!")
                break
            
            else:
                print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
