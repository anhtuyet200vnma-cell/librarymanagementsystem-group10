"""
BorrowRequest Model
- Mục đích: Đại diện cho yêu cầu mượn sách do Member tạo ra.
- Cần Admin duyệt thì mới tạo BorrowOrder.
"""

from datetime import date


REQUEST_STATUS = {
    "PENDING": "PENDING",
    "APPROVED": "APPROVED",
    "REJECTED": "REJECTED",
    "CANCELLED": "CANCELLED"
}


class BorrowRequest:
    """
    Theo tài liệu nhóm:
    - requestId, requestDate, status
    - requestedBy (Member)
    - books (List<Book>)
    - approvalDate (Optional)
    - approver (Admin)
    """

    def __init__(self, request_id: int, requested_by, books: list, request_date: date = None):
        # Validate request_id
        if not isinstance(request_id, int) or request_id <= 0:
            raise ValueError("request_id phải là số nguyên dương")

        # Validate books
        if not isinstance(books, list) or len(books) == 0:
            raise ValueError("BorrowRequest phải có ít nhất 1 book")

        self.request_id = request_id
        self.request_date = request_date if request_date else date.today()
        self.status = REQUEST_STATUS["PENDING"]

        # Liên kết người tạo request (Member)
        self.requested_by = requested_by

        # Danh sách sách yêu cầu mượn (có thể là list book_id hoặc object Book tùy nhóm)
        self.books = books

        # Khi PENDING thì chưa có
        self.approval_date = None
        self.approver = None

        # Nếu bị reject, lưu lý do
        self.reject_reason = None

    def get_status(self):
        """Trả về status hiện tại"""
        return self.status

    def cancel_request(self):
        """Member có quyền huỷ request khi đang PENDING"""
        if self.status != REQUEST_STATUS["PENDING"]:
            return False, "Chỉ được huỷ khi request đang PENDING"

        self.status = REQUEST_STATUS["CANCELLED"]
        return True, None

    def approve(self, admin):
        """
        Admin duyệt request.
        Sau khi approve, bên service sẽ tạo BorrowOrder.
        """
        if self.status != REQUEST_STATUS["PENDING"]:
            return False, "Chỉ được approve khi request đang PENDING"

        self.status = REQUEST_STATUS["APPROVED"]
        self.approval_date = date.today()
        self.approver = admin
        return True, None

    def reject(self, admin, reason: str):
        """Admin từ chối request"""
        if self.status != REQUEST_STATUS["PENDING"]:
            return False, "Chỉ được reject khi request đang PENDING"

        if not reason:
            return False, "Phải có lý do reject"

        self.status = REQUEST_STATUS["REJECTED"]
        self.approval_date = date.today()
        self.approver = admin
        self.reject_reason = reason
        return True, None

    def __str__(self):
        return f"BorrowRequest(id={self.request_id}, status={self.status}, books={len(self.books)})"
