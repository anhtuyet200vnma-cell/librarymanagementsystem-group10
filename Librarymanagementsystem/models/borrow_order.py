"""
BorrowOrder Model
- Đại diện cho phiếu mượn được tạo ra khi BorrowRequest APPROVED.
"""

from datetime import date
from .borrow_order_detail import BorrowOrderDetail


class BorrowOrder:
    def __init__(self, borrow_id: int, borrow_date: date, due_date: date, request_id: int = None):
        if not isinstance(borrow_id, int) or borrow_id <= 0:
            raise ValueError("borrow_id phải là số nguyên dương (>0)")

        if not isinstance(borrow_date, date):
            raise ValueError("borrow_date phải là kiểu datetime.date")

        if not isinstance(due_date, date):
            raise ValueError("due_date phải là kiểu datetime.date")

        if due_date < borrow_date:
            raise ValueError("due_date không được nhỏ hơn borrow_date")

        self.borrow_id = borrow_id
        self.borrow_date = borrow_date
        self.due_date = due_date

        # Liên kết BorrowRequest (theo data model có request_id FK)
        self.request_id = request_id

        # Danh sách sách mượn (composition 1..*)
        self.details: list[BorrowOrderDetail] = []

        # Trạng thái đơn
        self.return_date = None
        self.status = "Borrowed"

    def add_book(self, book_id: str):
        """Thêm sách vào đơn mượn"""
        self.details.append(BorrowOrderDetail(book_id))

    def mark_as_returned(self, return_date: date = None):
        """
        Đánh dấu toàn bộ đơn đã trả.
        Chỉ dùng khi tất cả sách trong details đã trả hoặc xử lý xong (lost/damaged).
        """
        if return_date is None:
            return_date = date.today()

        if return_date < self.borrow_date:
            raise ValueError("return_date không được nhỏ hơn borrow_date")

        self.return_date = return_date
        self.status = "Returned"

    def is_overdue(self, current_date: date = None) -> bool:
        """Đơn quá hạn nếu chưa trả và current_date > due_date"""
        if current_date is None:
            current_date = date.today()

        if self.status == "Returned":
            return False

        return current_date > self.due_date

    def calculate_overdue_days(self, current_date: date = None) -> int:
        """Tính số ngày trễ"""
        if current_date is None:
            current_date = date.today()

        end_date = self.return_date if self.return_date else current_date

        if end_date <= self.due_date:
            return 0

        return (end_date - self.due_date).days

    def get_status(self, current_date: date = None) -> str:
        """Trả về status theo logic chuẩn"""
        if self.status == "Returned":
            return "Returned"

        if self.is_overdue(current_date):
            return "Overdue"

        return "Borrowed"

    def __str__(self):
        return f"BorrowOrder(id={self.borrow_id}, status={self.get_status()}, books={len(self.details)})"
