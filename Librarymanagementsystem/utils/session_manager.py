"""
session_manager.py
Quản lý trạng thái đăng nhập trong chương trình.
"""

class SessionManager:
    """
    Class quản lý session (user đang đăng nhập).
    """

    def __init__(self):
        self.current_user = None
        self.user_role = None

    def login(self, user):
        """
        Gán user hiện tại sau khi đăng nhập thành công.
        """
        self.current_user = user
        self.user_role = user.role if hasattr(user, 'role') else None

    def logout(self):
        """
        Đăng xuất: xoá user hiện tại.
        """
        self.current_user = None
        self.user_role = None

    def is_logged_in(self) -> bool:
        """
        Kiểm tra có user đang đăng nhập hay không.
        """
        return self.current_user is not None

    def get_current_user(self):
        """
        Lấy user đang đăng nhập.
        """
        return self.current_user

    def is_admin(self) -> bool:
        """
        Kiểm tra user đang đăng nhập có phải admin không.
        """
        if self.current_user and hasattr(self.current_user, 'role'):
            return self.current_user.role.value == "ADMIN"
        return False

    def is_member(self) -> bool:
        """
        Kiểm tra user đang đăng nhập có phải member không.
        """
        if self.current_user and hasattr(self.current_user, 'role'):
            return self.current_user.role.value == "MEMBER"
        return False