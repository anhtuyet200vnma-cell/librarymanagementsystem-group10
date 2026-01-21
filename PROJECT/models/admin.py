# models/admin.py
from models.user import User

class Admin(User):
    def __init__(self, user_id, username, email, password, full_name, phone="", status="active"):
        # Gọi constructor của lớp cha
        super().__init__(user_id, username, email, password, full_name, phone, status, role="admin")
    
    def manage_books(self, action, book_data=None):
        """Quản lý sách: thêm, sửa, xóa"""
        actions = ["add", "edit", "delete", "view"]
        if action not in actions:
            return False, "Hành động không hợp lệ"
        
        # Ở đây sẽ gọi service sau
        return True, f"Đã {action} sách thành công"
    
    def manage_members(self, action, member_id=None, member_data=None):
        """Quản lý thành viên"""
        actions = ["view", "edit", "suspend", "activate"]
        if action not in actions:
            return False, "Hành động không hợp lệ"
        
        return True, f"Đã {action} thành viên {member_id}"
    
    def approve_borrow_request(self, request_id, decision):
        """Duyệt/từ chối yêu cầu mượn sách"""
        decisions = ["approve", "reject"]
        if decision not in decisions:
            return False, "Quyết định không hợp lệ"
        
        return True, f"Đã {decision} yêu cầu {request_id}"
    
    def display_admin_info(self):
        """Hiển thị thông tin admin"""
        base_info = super().display_info()
        return f"👑 {base_info} | Quyền: Quản trị hệ thống"