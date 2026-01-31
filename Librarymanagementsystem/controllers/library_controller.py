"""
library_controller.py
Controller chính để điều phối giữa UI và Services.
Đóng vai trò trung gian, xử lý logic nghiệp vụ phức tạp.
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.user_service import UserService
from services.book_service import BookService
from services.borrow_service import BorrowService
from services.admin_service import AdminService
from services.fine_service import FineService
from services.notification_service import NotificationService
from utils.session_manager import SessionManager
from utils.validator import Validator


class LibraryController:
    def __init__(self):
        """Khởi tạo controller với tất cả các service cần thiết"""
        self.session = SessionManager()
        self.user_service = UserService()
        self.book_service = BookService()
        self.borrow_service = BorrowService()
        self.admin_service = AdminService()
        self.fine_service = FineService()
        self.notification_service = NotificationService()
        self.validator = Validator()

    # ===== AUTHENTICATION =====
    def login(self, username: str, password: str) -> dict:
        """
        Đăng nhập vào hệ thống
        Returns: {"success": bool, "message": str, "user": User}
        """
        # Validate input
        if not username or not password:
            return {"success": False, "message": "Vui lòng nhập đầy đủ username và password"}
        
        # Call service
        result = self.user_service.login(username, password)
        
        if result.get("success"):
            user = result.get("user")
            self.session.login(user)
            
            # Send welcome notification
            self.notification_service.send_notification(
                user_id=user.user_id if hasattr(user, 'user_id') else 0,
                content=f"Chào mừng {user.username} đến với hệ thống thư viện!",
                notification_type="SYSTEM"
            )
            
            return {
                "success": True,
                "message": result.get("message"),
                "user": user,
                "role": user.role.value if hasattr(user, 'role') else "MEMBER"
            }
        
        return result

    def register(self, user_data: dict) -> dict:
        """
        Đăng ký tài khoản mới
        Returns: {"success": bool, "message": str, "user_id": int}
        """
        # Validate required fields
        required_fields = ["username", "password", "email"]
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                return {"success": False, "message": f"Thiếu trường bắt buộc: {field}"}
        
        # Validate username
        valid, msg = self.validator.validate_username(user_data["username"])
        if not valid:
            return {"success": False, "message": msg}
        
        # Validate password
        valid, msg = self.validator.validate_password(user_data["password"])
        if not valid:
            return {"success": False, "message": msg}
        
        # Validate email
        valid, msg = self.validator.validate_email(user_data["email"])
        if not valid:
            return {"success": False, "message": msg}
        
        # Check if passwords match (if confirm_password provided)
        if "confirm_password" in user_data and user_data["password"] != user_data["confirm_password"]:
            return {"success": False, "message": "Password và Confirm Password không khớp"}
        
        # Call service
        result = self.user_service.register(user_data)
        
        if result.get("success"):
            # Send welcome notification
            self.notification_service.send_notification(
                user_id=result.get("user_id", 0),
                content="Chào mừng bạn đến với hệ thống thư viện! Đăng ký thành công.",
                notification_type="SYSTEM"
            )
        
        return result

    def logout(self) -> dict:
        """
        Đăng xuất khỏi hệ thống
        """
        current_user = self.session.get_current_user()
        if current_user:
            user_id = current_user.user_id if hasattr(current_user, 'user_id') else 0
            self.notification_service.send_notification(
                user_id=user_id,
                content="Bạn đã đăng xuất khỏi hệ thống.",
                notification_type="SYSTEM"
            )
        
        self.session.logout()
        return {"success": True, "message": "Đăng xuất thành công"}

    # ===== BOOK MANAGEMENT =====
    def search_books(self, keyword: str) -> dict:
        """
        Tìm kiếm sách
        Returns: {"success": bool, "message": str, "books": list}
        """
        if not keyword or len(keyword.strip()) < 2:
            return {"success": False, "message": "Từ khóa tìm kiếm phải có ít nhất 2 ký tự"}
        
        try:
            books = self.book_service.search_books(keyword)
            return {
                "success": True,
                "message": f"Tìm thấy {len(books)} kết quả",
                "books": books
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi tìm kiếm: {str(e)}"}

    def get_book_details(self, book_id: str) -> dict:
        """
        Lấy chi tiết sách
        Returns: {"success": bool, "message": str, "book": Book}
        """
        if not book_id:
            return {"success": False, "message": "Thiếu Book ID"}
        
        try:
            book = self.book_service.get_book_by_id(book_id)
            if book:
                return {
                    "success": True,
                    "message": "Lấy thông tin sách thành công",
                    "book": book
                }
            else:
                return {"success": False, "message": f"Không tìm thấy sách với ID: {book_id}"}
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy thông tin sách: {str(e)}"}

    def get_all_books(self) -> dict:
        """
        Lấy tất cả sách
        Returns: {"success": bool, "message": str, "books": list}
        """
        try:
            books = self.book_service.get_all_books()
            return {
                "success": True,
                "message": f"Đã tải {len(books)} cuốn sách",
                "books": books
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi tải sách: {str(e)}"}

    def get_books_by_category(self, category_id: str) -> dict:
        """
        Lấy sách theo thể loại
        Returns: {"success": bool, "message": str, "books": list}
        """
        if not category_id:
            return {"success": False, "message": "Thiếu Category ID"}
        
        try:
            books = self.book_service.view_books_by_category(category_id)
            return {
                "success": True,
                "message": f"Tìm thấy {len(books)} sách trong thể loại này",
                "books": books
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy sách theo thể loại: {str(e)}"}

    def get_categories(self) -> dict:
        """
        Lấy danh sách thể loại
        Returns: {"success": bool, "message": str, "categories": list}
        """
        try:
            categories = self.book_service.get_categories()
            return {
                "success": True,
                "message": f"Đã tải {len(categories)} thể loại",
                "categories": categories
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy danh sách thể loại: {str(e)}"}

    # ===== BORROW MANAGEMENT =====
    def borrow_book(self, user_id: int, book_id: str) -> dict:
        """
        Mượn sách
        Returns: {"success": bool, "message": str, "borrow_id": str}
        """
        # Check if user is logged in
        if not self.session.is_logged_in():
            return {"success": False, "message": "Vui lòng đăng nhập trước khi mượn sách"}
        
        # Check if user is active
        current_user = self.session.get_current_user()
        if current_user and hasattr(current_user, 'status') and current_user.status.value != "ACTIVE":
            return {"success": False, "message": "Tài khoản của bạn không hoạt động"}
        
        # Validate inputs
        if not user_id or not book_id:
            return {"success": False, "message": "Thiếu thông tin User ID hoặc Book ID"}
        
        # Check if user has unpaid fines
        try:
            unpaid_fines = self.fine_service.get_unpaid_fines(user_id)
            if unpaid_fines:
                total_unpaid = sum(fine.get("amount", 0) for fine in unpaid_fines)
                return {
                    "success": False,
                    "message": f"Bạn có {len(unpaid_fines)} khoản phạt chưa thanh toán ({total_unpaid:,} VND). Vui lòng thanh toán trước khi mượn sách."
                }
        except:
            pass  # Ignore fine check errors
        
        # Call service
        result = self.borrow_service.borrow_book(user_id, book_id)
        
        if result.get("success"):
            # Send notification
            self.notification_service.send_borrow_confirmation(
                user_id=user_id,
                borrow_id=result.get("borrow_id", "")
            )
            
            # Check and send overdue notifications
            self._check_and_send_overdue_notifications(user_id)
        
        return result

    def return_book(self, borrow_id: str) -> dict:
        """
        Trả sách
        Returns: {"success": bool, "message": str}
        """
        if not borrow_id:
            return {"success": False, "message": "Thiếu mã đơn mượn"}
        
        # Call service
        result = self.borrow_service.return_book(borrow_id)
        
        if result.get("success"):
            # Get borrow details to find user_id
            try:
                borrows = self.borrow_service.get_user_borrows(0)  # Get all borrows
                for borrow in borrows:
                    if borrow.get("borrow_id") == borrow_id:
                        user_id = borrow.get("user_id")
                        # Send return confirmation
                        self.notification_service.send_return_confirmation(
                            user_id=user_id,
                            borrow_id=borrow_id
                        )
                        break
            except:
                pass  # Ignore notification errors
        
        return result

    def get_user_borrows(self, user_id: int) -> dict:
        """
        Lấy danh sách đơn mượn của user
        Returns: {"success": bool, "message": str, "borrows": list}
        """
        if not user_id:
            return {"success": False, "message": "Thiếu User ID"}
        
        try:
            borrows = self.borrow_service.get_user_borrows(user_id)
            return {
                "success": True,
                "message": f"Tìm thấy {len(borrows)} đơn mượn",
                "borrows": borrows
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy danh sách mượn: {str(e)}"}

    def get_current_borrows(self, user_id: int) -> dict:
        """
        Lấy danh sách sách đang mượn của user
        Returns: {"success": bool, "message": str, "borrows": list}
        """
        if not user_id:
            return {"success": False, "message": "Thiếu User ID"}
        
        try:
            borrows = self.borrow_service.get_user_borrows(user_id)
            current_borrows = [b for b in borrows if b.get("status") == "BORROWED"]
            return {
                "success": True,
                "message": f"Bạn đang mượn {len(current_borrows)} cuốn sách",
                "borrows": current_borrows
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy danh sách đang mượn: {str(e)}"}

    def get_overdue_borrows(self, user_id: int = None) -> dict:
        """
        Lấy danh sách đơn mượn quá hạn
        Returns: {"success": bool, "message": str, "borrows": list}
        """
        try:
            if user_id:
                borrows = self.borrow_service.get_user_borrows(user_id)
                now = datetime.now()
                overdue = []
                for borrow in borrows:
                    if borrow.get("status") == "BORROWED":
                        due_date_str = borrow.get("due_date")
                        if due_date_str:
                            try:
                                due_date = datetime.fromisoformat(due_date_str)
                                if due_date < now:
                                    overdue.append(borrow)
                            except:
                                pass
            else:
                overdue = self.borrow_service.get_overdue_borrows()
            
            return {
                "success": True,
                "message": f"Tìm thấy {len(overdue)} đơn mượn quá hạn",
                "borrows": overdue
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy danh sách quá hạn: {str(e)}"}

    # ===== ADMIN FUNCTIONS =====
    def admin_add_book(self, book_data: dict) -> dict:
        """
        Admin thêm sách mới
        Returns: {"success": bool, "message": str}
        """
        # Check if user is admin
        if not self._is_admin():
            return {"success": False, "message": "Chỉ Admin mới có quyền thêm sách"}
        
        # Validate required fields
        required_fields = ["book_id", "title", "quantity", "author_id", "category_id"]
        for field in required_fields:
            if field not in book_data or not book_data[field]:
                return {"success": False, "message": f"Thiếu trường bắt buộc: {field}"}
        
        # Validate quantity
        try:
            quantity = int(book_data["quantity"])
            if quantity <= 0:
                return {"success": False, "message": "Số lượng phải lớn hơn 0"}
        except:
            return {"success": False, "message": "Số lượng phải là số nguyên"}
        
        # Validate year
        if "publication_year" in book_data:
            try:
                year = int(book_data["publication_year"])
                if year < 1000 or year > 2100:
                    return {"success": False, "message": "Năm xuất bản không hợp lệ"}
            except:
                return {"success": False, "message": "Năm xuất bản phải là số"}
        
        # Set default values
        if "available_quantity" not in book_data:
            book_data["available_quantity"] = book_data["quantity"]
        if "available_copies" not in book_data:
            book_data["available_copies"] = book_data["quantity"]
        if "status" not in book_data:
            book_data["status"] = "AVAILABLE"
        
        # Call service
        try:
            success = self.admin_service.add_book(book_data)
            if success:
                return {"success": True, "message": f"Đã thêm sách '{book_data['title']}' thành công"}
            else:
                return {"success": False, "message": "Không thể thêm sách. Có thể Book ID đã tồn tại"}
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi thêm sách: {str(e)}"}

    def admin_delete_book(self, book_id: str) -> dict:
        """
        Admin xóa sách
        Returns: {"success": bool, "message": str}
        """
        # Check if user is admin
        if not self._is_admin():
            return {"success": False, "message": "Chỉ Admin mới có quyền xóa sách"}
        
        if not book_id:
            return {"success": False, "message": "Thiếu Book ID"}
        
        try:
            success = self.admin_service.delete_book(book_id)
            if success:
                return {"success": True, "message": f"Đã xóa sách '{book_id}' thành công"}
            else:
                return {"success": False, "message": f"Không thể xóa sách '{book_id}'. Có thể sách đang được mượn"}
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi xóa sách: {str(e)}"}

    def admin_update_book(self, book_id: str, update_data: dict) -> dict:
        """
        Admin cập nhật sách
        Returns: {"success": bool, "message": str}
        """
        # Check if user is admin
        if not self._is_admin():
            return {"success": False, "message": "Chỉ Admin mới có quyền cập nhật sách"}
        
        if not book_id:
            return {"success": False, "message": "Thiếu Book ID"}
        
        if not update_data:
            return {"success": False, "message": "Không có dữ liệu cập nhật"}
        
        # Validate quantity if provided
        if "quantity" in update_data:
            try:
                quantity = int(update_data["quantity"])
                if quantity <= 0:
                    return {"success": False, "message": "Số lượng phải lớn hơn 0"}
            except:
                return {"success": False, "message": "Số lượng phải là số nguyên"}
        
        try:
            success = self.admin_service.update_book(book_id, update_data)
            if success:
                return {"success": True, "message": f"Đã cập nhật sách '{book_id}' thành công"}
            else:
                return {"success": False, "message": f"Không thể cập nhật sách '{book_id}'"}
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi cập nhật sách: {str(e)}"}

    def admin_manage_user_status(self, user_id: int, status: str) -> dict:
        """
        Admin thay đổi trạng thái user
        Returns: {"success": bool, "message": str}
        """
        # Check if user is admin
        if not self._is_admin():
            return {"success": False, "message": "Chỉ Admin mới có quyền quản lý user"}
        
        if not user_id:
            return {"success": False, "message": "Thiếu User ID"}
        
        valid_statuses = ["ACTIVE", "INACTIVE", "SUSPENDED"]
        if status not in valid_statuses:
            return {"success": False, "message": f"Trạng thái không hợp lệ. Chọn từ: {', '.join(valid_statuses)}"}
        
        try:
            success = self.admin_service.manage_user_status(user_id, status)
            if success:
                # Send notification to user
                self.notification_service.send_notification(
                    user_id=user_id,
                    content=f"Trạng thái tài khoản của bạn đã được thay đổi thành: {status}",
                    notification_type="SYSTEM"
                )
                return {"success": True, "message": f"Đã cập nhật trạng thái user thành {status}"}
            else:
                return {"success": False, "message": "Không thể cập nhật trạng thái user"}
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi cập nhật trạng thái: {str(e)}"}

    def admin_get_system_stats(self) -> dict:
        """
        Admin lấy thống kê hệ thống
        Returns: {"success": bool, "message": str, "stats": dict}
        """
        # Check if user is admin
        if not self._is_admin():
            return {"success": False, "message": "Chỉ Admin mới có quyền xem thống kê"}
        
        try:
            stats = self.admin_service.get_system_stats()
            return {
                "success": True,
                "message": "Lấy thống kê thành công",
                "stats": stats
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy thống kê: {str(e)}"}

    def admin_search_users(self, keyword: str) -> dict:
        """
        Admin tìm kiếm user
        Returns: {"success": bool, "message": str, "users": list}
        """
        # Check if user is admin
        if not self._is_admin():
            return {"success": False, "message": "Chỉ Admin mới có quyền tìm kiếm user"}
        
        if not keyword:
            return {"success": False, "message": "Thiếu từ khóa tìm kiếm"}
        
        try:
            users = self.admin_service.search_user(keyword)
            return {
                "success": True,
                "message": f"Tìm thấy {len(users)} người dùng",
                "users": users
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi tìm kiếm user: {str(e)}"}

    def admin_get_all_users(self) -> dict:
        """
        Admin lấy tất cả users
        Returns: {"success": bool, "message": str, "users": list}
        """
        # Check if user is admin
        if not self._is_admin():
            return {"success": False, "message": "Chỉ Admin mới có quyền xem tất cả users"}
        
        try:
            users = self.admin_service.get_all_users()
            return {
                "success": True,
                "message": f"Đã tải {len(users)} người dùng",
                "users": users
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy danh sách users: {str(e)}"}

    def admin_get_all_books(self) -> dict:
        """
        Admin lấy tất cả sách (chi tiết)
        Returns: {"success": bool, "message": str, "books": list}
        """
        # Check if user is admin
        if not self._is_admin():
            return {"success": False, "message": "Chỉ Admin mới có quyền xem tất cả sách"}
        
        try:
            books = self.admin_service.get_all_books()
            return {
                "success": True,
                "message": f"Đã tải {len(books)} cuốn sách",
                "books": books
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy danh sách sách: {str(e)}"}

    def admin_view_all_borrows(self) -> dict:
        """
        Admin xem tất cả đơn mượn
        Returns: {"success": bool, "message": str, "borrows": list}
        """
        # Check if user is admin
        if not self._is_admin():
            return {"success": False, "message": "Chỉ Admin mới có quyền xem tất cả đơn mượn"}
        
        try:
            borrows = self.admin_service.view_all_borrows()
            return {
                "success": True,
                "message": f"Đã tải {len(borrows)} đơn mượn",
                "borrows": borrows
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy danh sách đơn mượn: {str(e)}"}

    def admin_view_all_fines(self) -> dict:
        """
        Admin xem tất cả tiền phạt
        Returns: {"success": bool, "message": str, "fines": list}
        """
        # Check if user is admin
        if not self._is_admin():
            return {"success": False, "message": "Chỉ Admin mới có quyền xem tất cả tiền phạt"}
        
        try:
            fines = self.admin_service.view_all_fines()
            return {
                "success": True,
                "message": f"Đã tải {len(fines)} khoản phạt",
                "fines": fines
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy danh sách phạt: {str(e)}"}

    # ===== FINE MANAGEMENT =====
    def get_user_fines(self, user_id: int) -> dict:
        """
        Lấy danh sách tiền phạt của user
        Returns: {"success": bool, "message": str, "fines": list}
        """
        if not user_id:
            return {"success": False, "message": "Thiếu User ID"}
        
        try:
            fines = self.fine_service.get_user_fines(user_id)
            unpaid_fines = [f for f in fines if not f.get("paid_status", False)]
            total_unpaid = sum(f.get("amount", 0) for f in unpaid_fines)
            
            return {
                "success": True,
                "message": f"Tìm thấy {len(fines)} khoản phạt ({len(unpaid_fines)} chưa thanh toán, tổng: {total_unpaid:,} VND)",
                "fines": fines,
                "total_unpaid": total_unpaid
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy danh sách phạt: {str(e)}"}

    def pay_fine(self, fine_id: str) -> dict:
        """
        Thanh toán tiền phạt
        Returns: {"success": bool, "message": str}
        """
        if not fine_id:
            return {"success": False, "message": "Thiếu mã phạt"}
        
        try:
            result = self.fine_service.pay_fine(fine_id)
            return result
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi thanh toán phạt: {str(e)}"}

    def calculate_overdue_fines(self) -> dict:
        """
        Tính và tạo tiền phạt quá hạn
        Returns: {"success": bool, "message": str, "fines_added": int}
        """
        try:
            fines_added = self.fine_service.calculate_overdue_fines()
            return {
                "success": True,
                "message": f"Đã tính và tạo {fines_added} khoản phạt quá hạn",
                "fines_added": fines_added
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi tính phạt quá hạn: {str(e)}"}

    # ===== NOTIFICATION MANAGEMENT =====
    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> dict:
        """
        Lấy thông báo của user
        Returns: {"success": bool, "message": str, "notifications": list}
        """
        if not user_id:
            return {"success": False, "message": "Thiếu User ID"}
        
        try:
            notifications = self.notification_service.get_user_notifications(user_id, unread_only)
            unread_count = len([n for n in notifications if not n.get("is_read", False)])
            
            return {
                "success": True,
                "message": f"Có {len(notifications)} thông báo ({unread_count} chưa đọc)",
                "notifications": notifications,
                "unread_count": unread_count
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lấy thông báo: {str(e)}"}

    def mark_notification_as_read(self, notification_id: str) -> dict:
        """
        Đánh dấu thông báo đã đọc
        Returns: {"success": bool, "message": str}
        """
        if not notification_id:
            return {"success": False, "message": "Thiếu mã thông báo"}
        
        try:
            success = self.notification_service.mark_as_read(notification_id)
            if success:
                return {"success": True, "message": "Đã đánh dấu đã đọc"}
            else:
                return {"success": False, "message": "Không tìm thấy thông báo"}
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi đánh dấu đã đọc: {str(e)}"}

    def mark_all_notifications_as_read(self, user_id: int) -> dict:
        """
        Đánh dấu tất cả thông báo của user là đã đọc
        Returns: {"success": bool, "message": str}
        """
        if not user_id:
            return {"success": False, "message": "Thiếu User ID"}
        
        try:
            success = self.notification_service.mark_all_as_read(user_id)
            if success:
                return {"success": True, "message": "Đã đánh dấu tất cả thông báo là đã đọc"}
            else:
                return {"success": False, "message": "Không có thông báo để đánh dấu"}
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi đánh dấu thông báo: {str(e)}"}

    def delete_notification(self, notification_id: str) -> dict:
        """
        Xóa thông báo
        Returns: {"success": bool, "message": str}
        """
        if not notification_id:
            return {"success": False, "message": "Thiếu mã thông báo"}
        
        try:
            success = self.notification_service.delete_notification(notification_id)
            if success:
                return {"success": True, "message": "Đã xóa thông báo"}
            else:
                return {"success": False, "message": "Không tìm thấy thông báo để xóa"}
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi xóa thông báo: {str(e)}"}

    # ===== USER PROFILE MANAGEMENT =====
    def get_current_user_info(self) -> dict:
        """
        Lấy thông tin user hiện tại
        Returns: {"success": bool, "message": str, "user": dict}
        """
        if not self.session.is_logged_in():
            return {"success": False, "message": "Chưa đăng nhập"}
        
        current_user = self.session.get_current_user()
        if current_user:
            user_info = {
                "user_id": current_user.user_id if hasattr(current_user, 'user_id') else 0,
                "username": current_user.username if hasattr(current_user, 'username') else "",
                "full_name": current_user.full_name if hasattr(current_user, 'full_name') else "",
                "email": current_user.email if hasattr(current_user, 'email') else "",
                "phone_number": current_user.phone_number if hasattr(current_user, 'phone_number') else "",
                "role": current_user.role.value if hasattr(current_user, 'role') else "MEMBER",
                "status": current_user.status.value if hasattr(current_user, 'status') else "ACTIVE"
            }
            
            # Add member-specific info
            if hasattr(current_user, 'borrowing_limit'):
                user_info["borrowing_limit"] = current_user.borrowing_limit
                user_info["penalty_status"] = current_user.penalty_status
            
            return {
                "success": True,
                "message": "Lấy thông tin user thành công",
                "user": user_info
            }
        
        return {"success": False, "message": "Không tìm thấy thông tin user"}

    def update_user_profile(self, user_id: int, update_data: dict) -> dict:
        """
        Cập nhật thông tin cá nhân
        Returns: {"success": bool, "message": str}
        """
        # Check if user is updating their own profile
        current_user = self.session.get_current_user()
        if not current_user:
            return {"success": False, "message": "Vui lòng đăng nhập"}
        
        current_user_id = current_user.user_id if hasattr(current_user, 'user_id') else 0
        if current_user_id != user_id and not self._is_admin():
            return {"success": False, "message": "Bạn chỉ có thể cập nhật thông tin của chính mình"}
        
        # Validate email if provided
        if "email" in update_data:
            valid, msg = self.validator.validate_email(update_data["email"])
            if not valid:
                return {"success": False, "message": msg}
        
        # Validate phone if provided
        if "phone_number" in update_data and update_data["phone_number"]:
            valid, msg = self.validator.validate_phone(update_data["phone_number"])
            if not valid:
                return {"success": False, "message": msg}
        
        # Call service
        result = self.user_service.update_profile(user_id, update_data)
        
        if result.get("success"):
            # Send notification
            self.notification_service.send_notification(
                user_id=user_id,
                content="Thông tin cá nhân của bạn đã được cập nhật",
                notification_type="SYSTEM"
            )
        
        return result

    def reset_password(self, user_id: int, old_password: str, new_password: str) -> dict:
        """
        Đổi mật khẩu
        Returns: {"success": bool, "message": str}
        """
        # Check if user is changing their own password
        current_user = self.session.get_current_user()
        if not current_user:
            return {"success": False, "message": "Vui lòng đăng nhập"}
        
        current_user_id = current_user.user_id if hasattr(current_user, 'user_id') else 0
        if current_user_id != user_id and not self._is_admin():
            return {"success": False, "message": "Bạn chỉ có thể đổi mật khẩu của chính mình"}
        
        # Validate new password
        valid, msg = self.validator.validate_password(new_password)
        if not valid:
            return {"success": False, "message": msg}
        
        # Call service
        result = self.user_service.reset_password(user_id, old_password, new_password)
        
        if result.get("success"):
            # Send notification
            self.notification_service.send_notification(
                user_id=user_id,
                content="Mật khẩu của bạn đã được thay đổi",
                notification_type="SYSTEM"
            )
        
        return result

    # ===== HELPER METHODS =====
    def _is_admin(self) -> bool:
        """Kiểm tra user hiện tại có phải admin không"""
        if not self.session.is_logged_in():
            return False
        
        current_user = self.session.get_current_user()
        if current_user and hasattr(current_user, 'role'):
            return current_user.role.value == "ADMIN"
        
        return False

    def _check_and_send_overdue_notifications(self, user_id: int):
        """Kiểm tra và gửi thông báo quá hạn"""
        try:
            borrows = self.borrow_service.get_user_borrows(user_id)
            for borrow in borrows:
                if borrow.get("status") == "BORROWED":
                    # Calculate overdue days
                    due_date_str = borrow.get("due_date")
                    if due_date_str:
                        due_date = datetime.fromisoformat(due_date_str)
                        if due_date < datetime.now():
                            overdue_days = (datetime.now() - due_date).days
                            if overdue_days > 0:
                                self.notification_service.send_overdue_notification(
                                    user_id=user_id,
                                    borrow_id=borrow.get("borrow_id", ""),
                                    overdue_days=overdue_days
                                )
        except:
            pass  # Ignore notification errors

    def check_user_can_borrow(self, user_id: int) -> dict:
        """
        Kiểm tra user có thể mượn sách không
        Returns: {"success": bool, "message": str, "can_borrow": bool}
        """
        try:
            # Check if user exists and is active
            user = self.user_service.get_user_by_id(user_id)
            if not user:
                return {"success": False, "message": "User không tồn tại", "can_borrow": False}
            
            # Check user status
            if hasattr(user, 'status') and user.status.value != "ACTIVE":
                return {"success": False, "message": "Tài khoản không hoạt động", "can_borrow": False}
            
            # Check penalty status
            if hasattr(user, 'penalty_status') and user.penalty_status:
                return {"success": False, "message": "Tài khoản đang bị phạt", "can_borrow": False}
            
            # Check borrowing limit
            borrows = self.borrow_service.get_user_borrows(user_id)
            current_borrows = len([b for b in borrows if b.get("status") == "BORROWED"])
            borrowing_limit = user.borrowing_limit if hasattr(user, 'borrowing_limit') else 5
            
            if current_borrows >= borrowing_limit:
                return {
                    "success": False,
                    "message": f"Đã đạt giới hạn mượn ({borrowing_limit} sách)",
                    "can_borrow": False,
                    "current_borrows": current_borrows,
                    "borrowing_limit": borrowing_limit
                }
            
            # Check unpaid fines
            unpaid_fines = self.fine_service.get_unpaid_fines(user_id)
            if unpaid_fines:
                total_unpaid = sum(f.get("amount", 0) for f in unpaid_fines)
                return {
                    "success": False,
                    "message": f"Có {len(unpaid_fines)} khoản phạt chưa thanh toán ({total_unpaid:,} VND)",
                    "can_borrow": False,
                    "unpaid_fines": len(unpaid_fines),
                    "total_unpaid": total_unpaid
                }
            
            return {
                "success": True,
                "message": "User có thể mượn sách",
                "can_borrow": True,
                "current_borrows": current_borrows,
                "borrowing_limit": borrowing_limit
            }
            
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi kiểm tra điều kiện mượn: {str(e)}", "can_borrow": False}