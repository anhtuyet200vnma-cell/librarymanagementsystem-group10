"""
validator.py
Các hàm kiểm tra dữ liệu (validate) trước khi tạo/ghi dữ liệu.
"""

from datetime import date
import re


class Validator:
    @staticmethod
    def validate_not_empty(value, field_name: str):
        """
        Check dữ liệu không được rỗng.
        """
        if value is None or str(value).strip() == "":
            return False, f"{field_name} không được để trống"
        return True, None

    @staticmethod
    def validate_positive_number(value, field_name: str):
        """
        Check số phải lớn hơn 0.
        """
        try:
            num = int(value)
            if num <= 0:
                return False, f"{field_name} phải lớn hơn 0"
            return True, None
        except:
            return False, f"{field_name} phải là số hợp lệ"

    @staticmethod
    def validate_non_negative_number(value, field_name: str):
        """
        Check số không âm (>= 0).
        """
        try:
            num = int(value)
            if num < 0:
                return False, f"{field_name} không được âm"
            return True, None
        except:
            return False, f"{field_name} phải là số hợp lệ"

    @staticmethod
    def validate_date_order(start_date: date, end_date: date, field_name: str = "Ngày"):
        """
        Check ngày kết thúc >= ngày bắt đầu.
        """
        if start_date is None or end_date is None:
            return True, None

        if end_date < start_date:
            return False, f"{field_name} không hợp lệ (ngày kết thúc nhỏ hơn ngày bắt đầu)"
        return True, None

    @staticmethod
    def validate_email(email: str):
        """
        Check email hợp lệ.
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            return False, "Email không hợp lệ"
        return True, None

    @staticmethod
    def validate_phone(phone: str):
        """
        Check số điện thoại Việt Nam hợp lệ.
        """
        pattern = r'^0\d{9,10}$'
        if not re.match(pattern, phone):
            return False, "Số điện thoại không hợp lệ (phải bắt đầu bằng 0 và có 10-11 số)"
        return True, None

    @staticmethod
    def validate_username(username: str):
        """
        Check username hợp lệ.
        """
        if len(username) < 3:
            return False, "Username phải có ít nhất 3 ký tự"
        if len(username) > 50:
            return False, "Username không được quá 50 ký tự"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username chỉ được chứa chữ cái, số và dấu gạch dưới"
        return True, None

    @staticmethod
    def validate_password(password: str):
        """
        Check password hợp lệ.
        """
        if len(password) < 8:
            return False, "Mật khẩu phải có ít nhất 8 ký tự"
        if len(password) > 100:
            return False, "Mật khẩu không được quá 100 ký tự"
        return True, None

    @staticmethod
    def validate_status(status: str, valid_statuses: list):
        """
        Check status hợp lệ.
        """
        if status not in valid_statuses:
            return False, f"Trạng thái không hợp lệ. Các trạng thái hợp lệ: {', '.join(valid_statuses)}"
        return True, None

    @staticmethod
    def validate_length(value: str, field_name: str, min_len: int = 1, max_len: int = 255):
        """
        Check độ dài chuỗi.
        """
        if len(value) < min_len:
            return False, f"{field_name} phải có ít nhất {min_len} ký tự"
        if len(value) > max_len:
            return False, f"{field_name} không được quá {max_len} ký tự"
        return True, None

    @staticmethod
    def validate_year(year: int, field_name: str = "Năm"):
        """
        Check năm hợp lệ.
        """
        current_year = date.today().year
        if year < 1000 or year > current_year + 5:
            return False, f"{field_name} không hợp lệ (phải từ 1000 đến {current_year + 5})"
        return True, None