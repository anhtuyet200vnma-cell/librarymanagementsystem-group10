# models/user.py
# Theo đặc tả trang 49
from datetime import datetime
from enum import Enum

class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"

class User:
    """
    USER class - Trang 49
    Base class representing all system users with authentication and profile management capabilities.
    """
    
    def __init__(self, user_id: int, username: str, password: str, email: str, 
                 full_name: str, phone_number: str = "", 
                 status: str = "ACTIVE"):
        """
        Khởi tạo User theo đặc tả trang 49
        
        Constraints:
        - userId: Integer, Primary Key, Auto-increment (trang 49)
        - username: String, Unique, Not null, 5-50 chars (trang 49)
        - password: String, Not null, Min 8 chars (trang 49)
        - email: String, Unique, Valid email format (trang 49)
        - fullName: String, Not null, 2-100 chars (trang 49)
        - phoneNumber: String, Optional, Valid phone format (trang 49)
        - status: String, Enum: ACTIVE, INACTIVE, SUSPENDED (trang 49)
        """
        
        # Validate theo đặc tả
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("user_id phải là số nguyên dương")
        
        if not isinstance(username, str) or not (5 <= len(username) <= 50):
            raise ValueError("username phải là chuỗi 5-50 ký tự")
        
        if not isinstance(password, str) or len(password) < 8:
            raise ValueError("password phải có ít nhất 8 ký tự")
        
        if not isinstance(email, str) or "@" not in email:
            raise ValueError("email phải có định dạng hợp lệ")
        
        if not isinstance(full_name, str) or not (2 <= len(full_name) <= 100):
            raise ValueError("full_name phải là chuỗi 2-100 ký tự")
        
        if not isinstance(phone_number, str):
            raise ValueError("phone_number phải là chuỗi")
        
        if status not in [s.value for s in AccountStatus]:
            raise ValueError(f"status phải là một trong: {[s.value for s in AccountStatus]}")
        
        # Gán thuộc tính
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.full_name = full_name
        self.phone_number = phone_number
        self.status = status
        self.created_at = datetime.now()
    
    # ===== METHODS THEO ĐẶC TẢ TRANG 49-50 =====
    
    def register_account(self, username: str, password: str, email: str, 
                        full_name: str, phone_number: str = "") -> bool:
        """
        Registers a new user account. Returns true on success.
        Theo đặc tả trang 49: registerAccount() method
        """
        # Logic đăng ký sẽ được xử lý trong service
        return True
    
    def login(self, username: str, password: str):
        """
        Authenticates the user and creates sessions.
        Theo đặc tả trang 50: login() method
        """
        if username == self.username and password == self.password:
            return {"user_id": self.user_id, "username": self.username}
        return None
    
    def logout(self, session_id: str) -> bool:
        """
        Terminates user session.
        Theo đặc tả trang 50: logout() method
        """
        return True
    
    def update_profile(self, email: str = None, full_name: str = None, 
                      phone_number: str = None) -> bool:
        """
        Updates user profile information.
        Theo đặc tả trang 50: updateProfile() method
        
        Note: Theo đặc tả trang 8: "Members can update information such as 
        phone number, address, and password (except for the username/email)"
        """
        if email:
            if "@" not in email:
                raise ValueError("Email không hợp lệ")
            self.email = email
        
        if full_name:
            if not (2 <= len(full_name) <= 100):
                raise ValueError("Họ tên phải từ 2-100 ký tự")
            self.full_name = full_name
        
        if phone_number:
            self.phone_number = phone_number
        
        return True
    
    def reset_password(self, email: str) -> bool:
        """
        Initiates password reset process.
        Theo đặc tả trang 50: resetPassword() method
        """
        if email == self.email:
            return True
        return False
    
    def to_dict(self):
        """Chuyển thành dictionary để lưu JSON"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Tạo User từ dictionary"""
        user = cls(
            user_id=data["user_id"],
            username=data["username"],
            password=data["password"],
            email=data["email"],
            full_name=data["full_name"],
            phone_number=data.get("phone_number", ""),
            status=data.get("status", "ACTIVE")
        )
        user.created_at = datetime.fromisoformat(data["created_at"])
        return user
    
    def __str__(self):
        return f"User(id={self.user_id}, username='{self.username}', email='{self.email}', status='{self.status}')"