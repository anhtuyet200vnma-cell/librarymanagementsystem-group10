# services/admin_service.py
from utils.file_handler_fix import load_json, save_json
from datetime import datetime, timedelta
import uuid
from config import MAX_BORROW_DAYS


class AdminService:
    def __init__(
        self,
        user_path="data/users.json",
        book_path="data/books.json",
        borrow_path="data/borrow_orders.json",
        fine_path="data/fines.json",
        author_path="data/authors.json",
        categories_file="data/categories.json"
    ):
        self.user_path = user_path
        self.book_path = book_path
        self.borrow_path = borrow_path
        self.fine_path = fine_path
        self.author_path = author_path
        self.categories_file = categories_file

    def add_book(self, book_data: dict) -> bool:
        """Admin thêm sách mới"""
        try:
            books = load_json(self.book_path)
            
            # Kiểm tra book_id đã tồn tại chưa
            existing_book = next((b for b in books if b.get("book_id") == book_data.get("book_id")), None)
            if existing_book:
                return False
            
            books.append(book_data)
            save_json(self.book_path, books)
            return True
        except Exception as e:
            print(f"Error adding book: {e}")
            return False

    def update_book(self, book_id: str, book_data: dict) -> bool:
        """Admin cập nhật thông tin sách"""
        try:
            books = load_json(self.book_path)
            
            for i, book in enumerate(books):
                if book.get("book_id") == book_id:
                    # Giữ lại book_id cũ
                    book_data["book_id"] = book_id
                    books[i] = {**book, **book_data}
                    save_json(self.book_path, books)
                    return True
            
            return False
        except Exception as e:
            print(f"Error updating book: {e}")
            return False

    def delete_book(self, book_id: str) -> bool:
        """Admin xóa sách"""
        try:
            books = load_json(self.book_path)
            
            filtered_books = [book for book in books if book.get("book_id") != book_id]
            
            if len(filtered_books) == len(books):
                return False  # Không tìm thấy sách
            
            save_json(self.book_path, filtered_books)
            return True
        except Exception as e:
            print(f"Error deleting book: {e}")
            return False

    def manage_user_status(self, user_id: int, status: str) -> bool:
        """Admin quản lý trạng thái user (ACTIVE/INACTIVE/SUSPENDED)"""
        try:
            users = load_json(self.user_path)
            
            for user in users:
                if user.get("user_id") == user_id:
                    if status not in ["ACTIVE", "INACTIVE", "SUSPENDED"]:
                        return False
                    user["status"] = status
                    save_json(self.user_path, users)
                    return True
            
            return False
        except Exception as e:
            print(f"Error managing user status: {e}")
            return False

    def view_all_borrows(self):
        """Admin xem tất cả đơn mượn"""
        try:
            borrows = load_json(self.borrow_path)
            return borrows
        except Exception as e:
            print(f"Error viewing borrows: {e}")
            return []

    def view_all_fines(self):
        """Admin xem tất cả tiền phạt"""
        try:
            fines = load_json(self.fine_path)
            return fines
        except Exception as e:
            print(f"Error viewing fines: {e}")
            return []

    def search_user(self, keyword: str):
        """Admin tìm kiếm user"""
        try:
            users = load_json(self.user_path)
            
            results = []
            for user in users:
                username = user.get("username", "").lower()
                email = user.get("email", "").lower()
                full_name = user.get("full_name", "").lower()
                keyword_lower = keyword.lower()
                
                if (keyword_lower in username or 
                    keyword_lower in email or 
                    keyword_lower in full_name):
                    results.append(user)
            
            return results
        except Exception as e:
            print(f"Error searching user: {e}")
            return []

    def get_system_stats(self):
        """Admin xem thống kê hệ thống"""
        try:
            users = load_json(self.user_path)
            books = load_json(self.book_path)
            borrows = load_json(self.borrow_path)
            fines = load_json(self.fine_path)
            
            # Tính số lượng admin và member
            admin_count = len([u for u in users if u.get("role") == "ADMIN"])
            member_count = len([u for u in users if u.get("role") == "MEMBER"])
            
            # Tính số đơn mượn đã trả
            returned_borrows = len([b for b in borrows if b.get("status") == "RETURNED"])
            
            # Tính số đơn mượn quá hạn
            from datetime import datetime
            now = datetime.now()
            overdue_borrows = 0
            for borrow in borrows:
                if borrow.get("status") == "BORROWED":
                    due_date_str = borrow.get("due_date")
                    if due_date_str:
                        try:
                            due_date = datetime.fromisoformat(due_date_str)
                            if due_date < now:
                                overdue_borrows += 1
                        except:
                            pass
            
            # Tính tổng tiền phạt chưa thanh toán
            unpaid_fines = sum(f.get("amount", 0) for f in fines if not f.get("paid_status", False))
            total_fines = sum(f.get("amount", 0) for f in fines)
            
            stats = {
                "total_users": len(users),
                "admin_count": admin_count,
                "member_count": member_count,
                "total_books": len(books),
                "active_borrows": len([b for b in borrows if b.get("status") == "BORROWED"]),
                "returned_borrows": returned_borrows,
                "overdue_borrows": overdue_borrows,
                "total_fines": total_fines,
                "unpaid_fines": unpaid_fines,
                "available_books": len([b for b in books if b.get("available_quantity", 0) > 0]),
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return stats
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}

    def get_all_users(self):
        """Lấy tất cả users"""
        try:
            users = load_json(self.user_path)
            return users
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    def get_all_books(self):
        """Lấy tất cả sách (cho admin)"""
        try:
            books = load_json(self.book_path)
            
            # Load authors for mapping
            authors_data = []
            try:
                authors_data = load_json(self.author_path)
            except:
                pass
            
            authors_map = {}
            for author in authors_data:
                authors_map[author.get("author_id")] = author.get("author_name", "Unknown")
            
            # Load categories for mapping
            categories_data = []
            try:
                categories_data = load_json(self.categories_file)
            except:
                pass
            
            categories_map = {}
            for category in categories_data:
                categories_map[category.get("category_id")] = category.get("category_name", "Unknown")
            
            # Add author and category names to books
            for book in books:
                book["author_name"] = authors_map.get(book.get("author_id"), "Unknown")
                book["category_name"] = categories_map.get(book.get("category_id"), "Unknown")
            
            return books
        except Exception as e:
            print(f"Error getting all books: {e}")
            return []