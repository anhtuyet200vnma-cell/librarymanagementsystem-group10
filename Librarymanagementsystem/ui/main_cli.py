"""
main_cli.py
Điểm khởi đầu cho giao diện dòng lệnh (CLI).
Chức năng: hiển thị menu chính và điều hướng các màn hình con.
"""

import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.user_service import UserService
from services.book_service import BookService
from services.borrow_service import BorrowService
from services.admin_service import AdminService
from utils.session_manager import SessionManager


class MainCLI:
    def __init__(self):
        self.session = SessionManager()
        self.user_service = UserService()
        self.book_service = BookService()
        self.borrow_service = BorrowService()
        self.admin_service = AdminService()
        self.current_user = None

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        """Hiển thị menu chính"""
        print("\n" + "="*50)
        print("          HỆ THỐNG QUẢN LÝ THƯ VIỆN")
        print("="*50)
        
        if self.current_user:
            print(f"Xin chào: {self.current_user.get('full_name', self.current_user.get('username', ''))}")
            print(f"Vai trò: {self.current_user.get('role', 'MEMBER')}")
            print("-"*50)
        
        print("1. Đăng nhập")
        print("2. Đăng ký")
        print("3. Quản lý sách")
        print("4. Quản lý mượn/trả")
        print("5. Quản trị hệ thống")
        print("6. Đăng xuất" if self.current_user else "")
        print("0. Thoát chương trình")
        print("="*50)

    def show_auth_menu(self):
        """Hiển thị menu đăng nhập/đăng ký"""
        self.clear_screen()
        print("\n" + "="*50)
        print("          ĐĂNG NHẬP / ĐĂNG KÝ")
        print("="*50)
        print("1. Đăng nhập")
        print("2. Đăng ký")
        print("3. Quay lại")
        print("="*50)

    def show_book_menu(self):
        """Hiển thị menu quản lý sách"""
        self.clear_screen()
        print("\n" + "="*50)
        print("          QUẢN LÝ SÁCH")
        print("="*50)
        print("1. Xem danh sách sách")
        print("2. Tìm kiếm sách")
        print("3. Xem chi tiết sách")
        print("4. Xem sách theo thể loại")
        print("5. Quay lại")
        print("="*50)

    def show_borrow_menu(self):
        """Hiển thị menu mượn/trả sách"""
        self.clear_screen()
        print("\n" + "="*50)
        print("          MƯỢN / TRẢ SÁCH")
        print("="*50)
        print("1. Mượn sách")
        print("2. Trả sách")
        print("3. Xem lịch sử mượn")
        print("4. Xem sách đang mượn")
        print("5. Quay lại")
        print("="*50)

    def show_admin_menu(self):
        """Hiển thị menu admin"""
        self.clear_screen()
        print("\n" + "="*50)
        print("          QUẢN TRỊ HỆ THỐNG")
        print("="*50)
        print("1. Thêm sách mới")
        print("2. Xóa sách")
        print("3. Cập nhật sách")
        print("4. Quản lý người dùng")
        print("5. Xem thống kê")
        print("6. Xem tất cả đơn mượn")
        print("7. Quay lại")
        print("="*50)

    def handle_login(self):
        """Xử lý đăng nhập"""
        self.clear_screen()
        print("\n" + "="*50)
        print("          ĐĂNG NHẬP")
        print("="*50)
        
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if not username or not password:
            print("❌ Vui lòng nhập đầy đủ thông tin!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        result = self.user_service.login(username, password)
        
        if result.get("success"):
            self.current_user = result.get("user").__dict__ if hasattr(result.get("user"), '__dict__') else result.get("user")
            self.session.login(result.get("user"))
            print(f"\n✅ {result.get('message')}")
            input("\nNhấn Enter để tiếp tục...")
        else:
            print(f"\n❌ {result.get('message')}")
            input("\nNhấn Enter để tiếp tục...")

    def handle_register(self):
        """Xử lý đăng ký"""
        self.clear_screen()
        print("\n" + "="*50)
        print("          ĐĂNG KÝ TÀI KHOẢN")
        print("="*50)
        
        username = input("Username (ít nhất 3 ký tự): ").strip()
        if len(username) < 3:
            print("❌ Username phải có ít nhất 3 ký tự!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        password = input("Password (ít nhất 8 ký tự): ").strip()
        if len(password) < 8:
            print("❌ Password phải có ít nhất 8 ký tự!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        confirm = input("Confirm Password: ").strip()
        if password != confirm:
            print("❌ Password và Confirm Password không khớp!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        full_name = input("Họ và tên: ").strip()
        email = input("Email: ").strip()
        phone = input("Số điện thoại (không bắt buộc): ").strip()
        
        user_data = {
            "username": username,
            "password": password,
            "email": email,
            "full_name": full_name,
            "phone_number": phone
        }
        
        result = self.user_service.register(user_data)
        
        if result.get("success"):
            print(f"\n✅ {result.get('message')}")
            print(f"   User ID của bạn là: {result.get('user_id')}")
        else:
            print(f"\n❌ {result.get('message')}")
        
        input("\nNhấn Enter để tiếp tục...")

    def handle_view_books(self):
        """Xem danh sách sách"""
        self.clear_screen()
        print("\n" + "="*50)
        print("          DANH SÁCH SÁCH")
        print("="*50)
        
        books = self.book_service.get_all_books()
        
        if not books:
            print("Không có sách nào trong hệ thống.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print(f"\nTổng số: {len(books)} cuốn sách\n")
        print("-"*100)
        print(f"{'ID':<10} {'Tiêu đề':<40} {'Tác giả':<20} {'Có sẵn':<10} {'Trạng thái':<15}")
        print("-"*100)
        
        for book in books:
            if hasattr(book, 'book_id'):
                status_text = "Có sẵn" if book.status == "AVAILABLE" else "Đã hết"
                print(f"{book.book_id:<10} {book.title[:38]:<40} {book.author.author_name[:18]:<20} "
                      f"{book.available_quantity:<10} {status_text:<15}")
        
        print("-"*100)
        input("\nNhấn Enter để tiếp tục...")

    def handle_search_books(self):
        """Tìm kiếm sách"""
        self.clear_screen()
        print("\n" + "="*50)
        print("          TÌM KIẾM SÁCH")
        print("="*50)
        
        keyword = input("Nhập từ khóa tìm kiếm: ").strip()
        
        if not keyword:
            print("❌ Vui lòng nhập từ khóa tìm kiếm!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        books = self.book_service.search_books(keyword)
        
        if not books:
            print(f"\nKhông tìm thấy sách nào với từ khóa '{keyword}'.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print(f"\nTìm thấy {len(books)} kết quả cho '{keyword}'\n")
        print("-"*100)
        print(f"{'ID':<10} {'Tiêu đề':<40} {'Tác giả':<20} {'Có sẵn':<10} {'Trạng thái':<15}")
        print("-"*100)
        
        for book in books:
            if hasattr(book, 'book_id'):
                status_text = "Có sẵn" if book.status == "AVAILABLE" else "Đã hết"
                print(f"{book.book_id:<10} {book.title[:38]:<40} {book.author.author_name[:18]:<20} "
                      f"{book.available_quantity:<10} {status_text:<15}")
        
        print("-"*100)
        input("\nNhấn Enter để tiếp tục...")

    def handle_book_details(self):
        """Xem chi tiết sách"""
        self.clear_screen()
        print("\n" + "="*50)
        print("          CHI TIẾT SÁCH")
        print("="*50)
        
        book_id = input("Nhập Book ID: ").strip()
        
        if not book_id:
            print("❌ Vui lòng nhập Book ID!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        book = self.book_service.get_book_by_id(book_id)
        
        if not book:
            print(f"❌ Không tìm thấy sách với ID '{book_id}'")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print("\n" + "="*50)
        print("          THÔNG TIN SÁCH")
        print("="*50)
        print(f"Mã sách: {book.book_id}")
        print(f"Tiêu đề: {book.title}")
        print(f"Tác giả: {book.author.author_name if hasattr(book.author, 'author_name') else 'Unknown'}")
        print(f"Mô tả: {book.description[:100]}..." if len(book.description) > 100 else f"Mô tả: {book.description}")
        print(f"Năm xuất bản: {book.publication_year}")
        print(f"Tổng số lượng: {book.quantity}")
        print(f"Số lượng có sẵn: {book.available_quantity}")
        print(f"Trạng thái: {book.status}")
        print("="*50)
        
        input("\nNhấn Enter để tiếp tục...")

    def handle_borrow_book(self):
        """Xử lý mượn sách"""
        if not self.current_user:
            print("❌ Vui lòng đăng nhập trước khi mượn sách!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        self.clear_screen()
        print("\n" + "="*50)
        print("          MƯỢN SÁCH")
        print("="*50)
        
        print(f"User ID: {self.current_user.get('user_id', '')}")
        book_id = input("Nhập Book ID: ").strip()
        
        if not book_id:
            print("❌ Vui lòng nhập Book ID!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        user_id = self.current_user.get('user_id')
        result = self.borrow_service.borrow_book(user_id, book_id)
        
        if result.get("success"):
            print(f"\n✅ {result.get('message')}")
            print(f"   Mã đơn mượn: {result.get('borrow_id')}")
        else:
            print(f"\n❌ {result.get('message')}")
        
        input("\nNhấn Enter để tiếp tục...")

    def handle_return_book(self):
        """Xử lý trả sách"""
        if not self.current_user:
            print("❌ Vui lòng đăng nhập trước khi trả sách!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        self.clear_screen()
        print("\n" + "="*50)
        print("          TRẢ SÁCH")
        print("="*50)
        
        borrow_id = input("Nhập mã đơn mượn: ").strip()
        
        if not borrow_id:
            print("❌ Vui lòng nhập mã đơn mượn!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        result = self.borrow_service.return_book(borrow_id)
        
        if result.get("success"):
            print(f"\n✅ {result.get('message')}")
        else:
            print(f"\n❌ {result.get('message')}")
        
        input("\nNhấn Enter để tiếp tục...")

    def handle_view_borrow_history(self):
        """Xem lịch sử mượn"""
        if not self.current_user:
            print("❌ Vui lòng đăng nhập để xem lịch sử!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        self.clear_screen()
        print("\n" + "="*50)
        print("          LỊCH SỬ MƯỢN SÁCH")
        print("="*50)
        
        user_id = self.current_user.get('user_id')
        borrows = self.borrow_service.get_user_borrows(user_id)
        
        if not borrows:
            print("Bạn chưa có đơn mượn nào.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print(f"\nTổng số: {len(borrows)} đơn mượn\n")
        print("-"*120)
        print(f"{'Mã mượn':<15} {'Ngày mượn':<15} {'Hạn trả':<15} {'Ngày trả':<15} {'Trạng thái':<20} {'Sách':<30}")
        print("-"*120)
        
        for borrow in borrows:
            status_text = {
                "BORROWED": "Đang mượn",
                "RETURNED": "Đã trả",
                "OVERDUE": "Quá hạn"
            }.get(borrow.get("status", ""), borrow.get("status", ""))
            
            books_str = ", ".join(borrow.get("books", []))[:28]
            borrow_date = borrow.get("borrow_date", "")[:10] if borrow.get("borrow_date") else ""
            due_date = borrow.get("due_date", "")[:10] if borrow.get("due_date") else ""
            return_date = borrow.get("return_date", "")[:10] if borrow.get("return_date") else ""
            
            print(f"{borrow.get('borrow_id', '')[:12]:<15} {borrow_date:<15} {due_date:<15} {return_date:<15} "
                  f"{status_text:<20} {books_str:<30}")
        
        print("-"*120)
        input("\nNhấn Enter để tiếp tục...")

    def handle_admin_add_book(self):
        """Admin thêm sách mới"""
        if not self.current_user or self.current_user.get('role') != 'ADMIN':
            print("❌ Chỉ Admin mới có quyền này!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        self.clear_screen()
        print("\n" + "="*50)
        print("          THÊM SÁCH MỚI")
        print("="*50)
        
        book_id = input("Mã sách: ").strip()
        title = input("Tiêu đề: ").strip()
        author_id = input("Mã tác giả: ").strip()
        category_id = input("Mã thể loại: ").strip()
        quantity = input("Số lượng: ").strip()
        year = input("Năm xuất bản: ").strip()
        description = input("Mô tả: ").strip()
        
        if not all([book_id, title, author_id, category_id, quantity, year]):
            print("❌ Vui lòng điền đầy đủ thông tin!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        if not quantity.isdigit() or int(quantity) <= 0:
            print("❌ Số lượng phải là số dương!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        if not year.isdigit() or int(year) < 1000:
            print("❌ Năm xuất bản không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        book_data = {
            "book_id": book_id,
            "title": title,
            "description": description,
            "publication_year": int(year),
            "quantity": int(quantity),
            "available_quantity": int(quantity),
            "available_copies": int(quantity),
            "status": "AVAILABLE",
            "author_id": int(author_id) if author_id.isdigit() else author_id,
            "category_id": category_id
        }
        
        success = self.admin_service.add_book(book_data)
        
        if success:
            print(f"\n✅ Đã thêm sách '{title}' thành công!")
        else:
            print(f"\n❌ Không thể thêm sách. Có thể Book ID đã tồn tại.")
        
        input("\nNhấn Enter để tiếp tục...")

    def handle_admin_stats(self):
        """Admin xem thống kê"""
        if not self.current_user or self.current_user.get('role') != 'ADMIN':
            print("❌ Chỉ Admin mới có quyền này!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        self.clear_screen()
        print("\n" + "="*50)
        print("          THỐNG KÊ HỆ THỐNG")
        print("="*50)
        
        stats = self.admin_service.get_system_stats()
        
        if not stats:
            print("Không thể lấy thống kê.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print(f"\n📚 SÁCH:")
        print(f"  • Tổng số sách: {stats.get('total_books', 0):,}")
        print(f"  • Sách có sẵn: {stats.get('available_books', 0):,}")
        
        print(f"\n👥 NGƯỜI DÙNG:")
        print(f"  • Tổng số người dùng: {stats.get('total_users', 0):,}")
        
        print(f"\n📊 HOẠT ĐỘNG:")
        print(f"  • Đang mượn: {stats.get('active_borrows', 0):,}")
        print(f"  • Quá hạn: {stats.get('total_fines', 0):,}")
        
        input("\nNhấn Enter để tiếp tục...")

    def handle_admin_manage_users(self):
        """Admin quản lý người dùng"""
        if not self.current_user or self.current_user.get('role') != 'ADMIN':
            print("❌ Chỉ Admin mới có quyền này!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        self.clear_screen()
        print("\n" + "="*50)
        print("          QUẢN LÝ NGƯỜI DÙNG")
        print("="*50)
        
        keyword = input("Nhập từ khóa tìm kiếm (Enter để xem tất cả): ").strip()
        
        if keyword:
            users = self.admin_service.search_users(keyword)
        else:
            users = self.admin_service.get_all_users()
        
        if not users:
            print("Không tìm thấy người dùng nào.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print(f"\nTìm thấy {len(users)} người dùng\n")
        print("-"*80)
        print(f"{'ID':<5} {'Username':<15} {'Họ tên':<20} {'Email':<25} {'Vai trò':<10} {'Trạng thái':<10}")
        print("-"*80)
        
        for user in users:
            role_text = "Admin" if user.get("role") == "ADMIN" else "Member"
            status_text = {
                "ACTIVE": "Hoạt động",
                "INACTIVE": "Không HĐ",
                "SUSPENDED": "Tạm khóa"
            }.get(user.get("status", ""), user.get("status", ""))
            
            print(f"{user.get('user_id', ''):<5} {user.get('username', '')[:13]:<15} "
                  f"{user.get('full_name', '')[:18]:<20} {user.get('email', '')[:23]:<25} "
                  f"{role_text:<10} {status_text:<10}")
        
        print("-"*80)
        
        # Option to change status
        user_id = input("\nNhập User ID để thay đổi trạng thái (Enter để bỏ qua): ").strip()
        
        if user_id and user_id.isdigit():
            print("\nChọn trạng thái mới:")
            print("1. ACTIVE - Hoạt động")
            print("2. INACTIVE - Không hoạt động")
            print("3. SUSPENDED - Tạm khóa")
            
            choice = input("Chọn (1-3): ").strip()
            
            status_map = {"1": "ACTIVE", "2": "INACTIVE", "3": "SUSPENDED"}
            new_status = status_map.get(choice)
            
            if new_status:
                success = self.admin_service.manage_user_status(int(user_id), new_status)
                if success:
                    print(f"\n✅ Đã cập nhật trạng thái thành {new_status}")
                else:
                    print(f"\n❌ Không thể cập nhật trạng thái")
            else:
                print("\n❌ Lựa chọn không hợp lệ")
        
        input("\nNhấn Enter để tiếp tục...")

    def run(self):
        """Chạy vòng lặp chính của chương trình"""
        while True:
            self.clear_screen()
            self.show_menu()
            choice = input("\nChọn chức năng: ").strip()

            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_register()
            elif choice == "3":
                self.handle_book_management()
            elif choice == "4":
                self.handle_borrow_management()
            elif choice == "5":
                self.handle_admin_management()
            elif choice == "6" and self.current_user:
                self.current_user = None
                self.session.logout()
                print("\n✅ Đã đăng xuất thành công!")
                input("\nNhấn Enter để tiếp tục...")
            elif choice == "0":
                print("\n👋 Thoát chương trình. Tạm biệt!")
                break
            else:
                print("\n❌ Lựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")

    def handle_book_management(self):
        """Xử lý menu quản lý sách"""
        while True:
            self.show_book_menu()
            choice = input("\nChọn chức năng: ").strip()

            if choice == "1":
                self.handle_view_books()
            elif choice == "2":
                self.handle_search_books()
            elif choice == "3":
                self.handle_book_details()
            elif choice == "4":
                self.handle_books_by_category()
            elif choice == "5":
                break
            else:
                print("\n❌ Lựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")

    def handle_borrow_management(self):
        """Xử lý menu mượn/trả sách"""
        while True:
            self.show_borrow_menu()
            choice = input("\nChọn chức năng: ").strip()

            if choice == "1":
                self.handle_borrow_book()
            elif choice == "2":
                self.handle_return_book()
            elif choice == "3":
                self.handle_view_borrow_history()
            elif choice == "4":
                self.handle_current_borrows()
            elif choice == "5":
                break
            else:
                print("\n❌ Lựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")

    def handle_admin_management(self):
        """Xử lý menu admin"""
        while True:
            self.show_admin_menu()
            choice = input("\nChọn chức năng: ").strip()

            if choice == "1":
                self.handle_admin_add_book()
            elif choice == "2":
                self.handle_admin_delete_book()
            elif choice == "3":
                self.handle_admin_update_book()
            elif choice == "4":
                self.handle_admin_manage_users()
            elif choice == "5":
                self.handle_admin_stats()
            elif choice == "6":
                self.handle_admin_view_all_borrows()
            elif choice == "7":
                break
            else:
                print("\n❌ Lựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")

    def handle_books_by_category(self):
        """Xem sách theo thể loại"""
        self.clear_screen()
        print("\n" + "="*50)
        print("          SÁCH THEO THỂ LOẠI")
        print("="*50)
        
        # In danh sách thể loại
        categories = self.book_service.get_categories()
        if categories:
            print("\nDanh sách thể loại:")
            for cat in categories:
                print(f"  {cat.get('category_id')}: {cat.get('category_name')}")
        
        category_id = input("\nNhập mã thể loại: ").strip()
        
        if not category_id:
            print("❌ Vui lòng nhập mã thể loại!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        books = self.book_service.view_books_by_category(category_id)
        
        if not books:
            print(f"\nKhông có sách nào trong thể loại '{category_id}'.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print(f"\nTổng số: {len(books)} cuốn sách trong thể loại '{category_id}'\n")
        print("-"*100)
        print(f"{'ID':<10} {'Tiêu đề':<40} {'Tác giả':<20} {'Có sẵn':<10} {'Trạng thái':<15}")
        print("-"*100)
        
        for book in books:
            if hasattr(book, 'book_id'):
                status_text = "Có sẵn" if book.status == "AVAILABLE" else "Đã hết"
                print(f"{book.book_id:<10} {book.title[:38]:<40} {book.author.author_name[:18]:<20} "
                      f"{book.available_quantity:<10} {status_text:<15}")
        
        print("-"*100)
        input("\nNhấn Enter để tiếp tục...")

    def handle_current_borrows(self):
        """Xem sách đang mượn"""
        if not self.current_user:
            print("❌ Vui lòng đăng nhập!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        self.clear_screen()
        print("\n" + "="*50)
        print("          SÁCH ĐANG MƯỢN")
        print("="*50)
        
        user_id = self.current_user.get('user_id')
        borrows = self.borrow_service.get_user_borrows(user_id)
        
        if not borrows:
            print("Bạn không có sách nào đang mượn.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        current_borrows = [b for b in borrows if b.get("status") == "BORROWED"]
        
        if not current_borrows:
            print("Bạn không có sách nào đang mượn.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print(f"\nBạn đang mượn {len(current_borrows)} cuốn sách:\n")
        print("-"*80)
        print(f"{'Mã mượn':<15} {'Ngày mượn':<15} {'Hạn trả':<15} {'Sách':<30}")
        print("-"*80)
        
        for borrow in current_borrows:
            books_str = ", ".join(borrow.get("books", []))[:28]
            borrow_date = borrow.get("borrow_date", "")[:10] if borrow.get("borrow_date") else ""
            due_date = borrow.get("due_date", "")[:10] if borrow.get("due_date") else ""
            
            print(f"{borrow.get('borrow_id', '')[:12]:<15} {borrow_date:<15} {due_date:<15} {books_str:<30}")
        
        print("-"*80)
        input("\nNhấn Enter để tiếp tục...")

    def handle_admin_delete_book(self):
        """Admin xóa sách"""
        if not self.current_user or self.current_user.get('role') != 'ADMIN':
            print("❌ Chỉ Admin mới có quyền này!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        self.clear_screen()
        print("\n" + "="*50)
        print("          XÓA SÁCH")
        print("="*50)
        
        self.handle_view_books()
        
        book_id = input("\nNhập Book ID cần xóa: ").strip()
        
        if not book_id:
            print("❌ Vui lòng nhập Book ID!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        confirm = input(f"Bạn có chắc muốn xóa sách '{book_id}'? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("Đã hủy thao tác xóa.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        success = self.admin_service.delete_book(book_id)
        
        if success:
            print(f"\n✅ Đã xóa sách '{book_id}' thành công!")
        else:
            print(f"\n❌ Không thể xóa sách '{book_id}'")
        
        input("\nNhấn Enter để tiếp tục...")

    def handle_admin_update_book(self):
        """Admin cập nhật sách"""
        if not self.current_user or self.current_user.get('role') != 'ADMIN':
            print("❌ Chỉ Admin mới có quyền này!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        self.clear_screen()
        print("\n" + "="*50)
        print("          CẬP NHẬT SÁCH")
        print("="*50)
        
        book_id = input("Nhập Book ID cần cập nhật: ").strip()
        
        if not book_id:
            print("❌ Vui lòng nhập Book ID!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        book = self.book_service.get_book_by_id(book_id)
        
        if not book:
            print(f"❌ Không tìm thấy sách với ID '{book_id}'")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print(f"\nThông tin hiện tại của sách '{book.title}':")
        print(f"  Tiêu đề: {book.title}")
        print(f"  Số lượng: {book.quantity}")
        print(f"  Số lượng có sẵn: {book.available_quantity}")
        print(f"  Trạng thái: {book.status}")
        
        print("\nNhập thông tin mới (Enter để giữ nguyên):")
        new_title = input(f"Tiêu đề mới [{book.title}]: ").strip()
        new_quantity = input(f"Số lượng mới [{book.quantity}]: ").strip()
        new_status = input(f"Trạng thái mới (AVAILABLE/UNAVAILABLE) [{book.status}]: ").strip().upper()
        
        update_data = {}
        if new_title:
            update_data["title"] = new_title
        if new_quantity and new_quantity.isdigit():
            update_data["quantity"] = int(new_quantity)
            update_data["available_quantity"] = int(new_quantity)
        if new_status in ["AVAILABLE", "UNAVAILABLE"]:
            update_data["status"] = new_status
        
        if not update_data:
            print("\nKhông có thay đổi nào được thực hiện.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        success = self.admin_service.update_book(book_id, update_data)
        
        if success:
            print(f"\n✅ Đã cập nhật sách '{book_id}' thành công!")
        else:
            print(f"\n❌ Không thể cập nhật sách '{book_id}'")
        
        input("\nNhấn Enter để tiếp tục...")

    def handle_admin_view_all_borrows(self):
        """Admin xem tất cả đơn mượn"""
        if not self.current_user or self.current_user.get('role') != 'ADMIN':
            print("❌ Chỉ Admin mới có quyền này!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        self.clear_screen()
        print("\n" + "="*50)
        print("          TẤT CẢ ĐƠN MƯỢN")
        print("="*50)
        
        borrows = self.admin_service.view_all_borrows()
        
        if not borrows:
            print("Không có đơn mượn nào trong hệ thống.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print(f"\nTổng số: {len(borrows)} đơn mượn\n")
        print("-"*120)
        print(f"{'Mã mượn':<15} {'User ID':<8} {'Ngày mượn':<15} {'Hạn trả':<15} {'Ngày trả':<15} {'Trạng thái':<20} {'Sách':<30}")
        print("-"*120)
        
        for borrow in borrows:
            status_text = {
                "BORROWED": "Đang mượn",
                "RETURNED": "Đã trả",
                "OVERDUE": "Quá hạn"
            }.get(borrow.get("status", ""), borrow.get("status", ""))
            
            books_str = ", ".join(borrow.get("books", []))[:28]
            borrow_date = borrow.get("borrow_date", "")[:10] if borrow.get("borrow_date") else ""
            due_date = borrow.get("due_date", "")[:10] if borrow.get("due_date") else ""
            return_date = borrow.get("return_date", "")[:10] if borrow.get("return_date") else ""
            
            print(f"{borrow.get('borrow_id', '')[:12]:<15} {borrow.get('user_id', ''):<8} "
                  f"{borrow_date:<15} {due_date:<15} {return_date:<15} "
                  f"{status_text:<20} {books_str:<30}")
        
        print("-"*120)
        
        # Show overdue borrows
        overdue = self.borrow_service.get_overdue_borrows()
        if overdue:
            print(f"\n⚠️  Cảnh báo: Có {len(overdue)} đơn mượn quá hạn!")
        
        input("\nNhấn Enter để tiếp tục...")


# Helper function to get categories (need to add to BookService)
def add_get_categories_method():
    """Add get_categories method to BookService if not exists"""
    from services.book_service import BookService
    import json
    import os
    
    def get_categories(self):
        """Get all categories"""
        try:
            categories_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data", "categories.json"
            )
            if os.path.exists(categories_file):
                with open(categories_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except:
            pass
        return []
    
    # Add method if not exists
    if not hasattr(BookService, 'get_categories'):
        BookService.get_categories = get_categories


if __name__ == "__main__":
    # Add get_categories method
    add_get_categories_method()
    
    # Run CLI application
    app = MainCLI()
    app.run()