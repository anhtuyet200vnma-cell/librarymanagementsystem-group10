# models/admin.py
# Theo đặc tả trang 50-51
from models.user import User

class Admin(User):
    """
    ADMIN Class - Trang 50-51
    System administrator inheriting from USER with extended privileges for system management.
    """
    
    def __init__(self, user_id: int, username: str, password: str, email: str, 
                 full_name: str, phone_number: str = "", status: str = "ACTIVE"):
        """
        Khởi tạo Admin
        Admin kế thừa tất cả thuộc tính từ User
        """
        super().__init__(user_id, username, password, email, full_name, 
                        phone_number, status)
        self.role = "ADMIN"  # Theo đặc tả trang 71: Role phân biệt Admin/Member
    
    # ===== METHODS THEO ĐẶC TẢ TRANG 50 =====
    
    def manage_books(self, book_data: dict, operation: str) -> bool:
        """
        CRUD operations for books (Add/Edit/Delete).
        Theo đặc tả trang 50: manageBooks() method
        
        Operation: "add", "edit", "delete", "view"
        Theo đặc tả trang 9: "Admins can add new books, edit book information, 
        delete books from the system, and display a list of books"
        """
        valid_operations = ["add", "edit", "delete", "view"]
        if operation not in valid_operations:
            raise ValueError(f"Operation phải là một trong: {valid_operations}")
        
        # Logic quản lý sách sẽ được xử lý trong service
        return True
    
    def manage_borrow_return(self, borrow_id: int, action: str) -> bool:
        """
        Processes borrow/return operations.
        Theo đặc tả trang 50: manageBorrowReturn() method
        
        Theo đặc tả trang 9: "Admins are able to manage borrow/return orders: 
        track all book borrowing transactions, update the book status when 
        members borrow or return books"
        """
        valid_actions = ["approve", "reject", "process_return", "track"]
        if action not in valid_actions:
            raise ValueError(f"Action phải là một trong: {valid_actions}")
        
        # Logic sẽ được xử lý trong service
        return True
    
    def manage_members(self, member_id: int, action: str, data: dict = None) -> bool:
        """
        Manages member accounts (Approve/Suspend/Update).
        Theo đặc tả trang 51: manageMembers() method
        
        Theo đặc tả trang 9: "Admins can view, add, edit, and delete member accounts."
        """
        valid_actions = ["view", "add", "edit", "delete", "suspend", "activate"]
        if action not in valid_actions:
            raise ValueError(f"Action phải là một trong: {valid_actions}")
        
        # Logic sẽ được xử lý trong service
        return True
    
    # ===== PRIVILEGES THEO ĐẶC TẢ TRANG 51 =====
    
    def has_full_access(self) -> bool:
        """Full access to all system modules - Trang 51"""
        return True
    
    def can_override_borrowing_limits(self) -> bool:
        """Can override borrowing limits - Trang 51"""
        return True
    
    def can_waive_or_modify_fines(self) -> bool:
        """Can waive or modify fines - Trang 51"""
        return True
    
    def can_manage_all_users(self) -> bool:
        """Can manage all user accounts - Trang 51"""
        return True
    
    def can_configure_system(self) -> bool:
        """Can configure system parameters - Trang 51"""
        return True
    
    def approve_borrow_request(self, request_id: int, decision: str) -> bool:
        """
        Duyệt/từ chối yêu cầu mượn sách
        Theo đặc tả trang 9: "Admins can approve or reject borrowing requests."
        """
        if decision not in ["approve", "reject"]:
            raise ValueError("Decision phải là 'approve' hoặc 'reject'")
        
        return True
    
    def to_dict(self):
        """Chuyển thành dictionary"""
        data = super().to_dict()
        data["role"] = self.role
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Tạo Admin từ dictionary"""
        admin = cls(
            user_id=data["user_id"],
            username=data["username"],
            password=data["password"],
            email=data["email"],
            full_name=data["full_name"],
            phone_number=data.get("phone_number", ""),
            status=data.get("status", "ACTIVE")
        )
        admin.created_at = datetime.fromisoformat(data["created_at"])
        return admin
    
    def __str__(self):
        return f"Admin(id={self.user_id}, username='{self.username}', privileges=full_access)"