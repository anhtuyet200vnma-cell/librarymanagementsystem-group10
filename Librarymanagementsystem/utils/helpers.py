"""
helpers.py
Các hàm tiện ích dùng chung cho toàn bộ hệ thống.
"""

from datetime import datetime, date
import random
import string


def generate_id(prefix: str = "", length: int = 6) -> str:
    """
    Tạo ID ngẫu nhiên.
    Ví dụ: generate_id("B") -> "B5F8K2A"
    """
    chars = string.ascii_uppercase + string.digits
    random_part = "".join(random.choices(chars, k=length))
    return f"{prefix}{random_part}"


def get_current_datetime() -> str:
    """
    Trả về datetime hiện tại dạng chuỗi ISO.
    Ví dụ: 2026-01-23T14:20:30
    """
    return datetime.now().isoformat(timespec="seconds")


def get_current_date() -> str:
    """
    Trả về ngày hiện tại dạng YYYY-MM-DD
    """
    return date.today().isoformat()


def parse_date_str(date_str: str) -> date:
    """
    Chuyển chuỗi YYYY-MM-DD thành đối tượng date.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return date.today()


def format_currency(amount: int) -> str:
    """
    Format tiền Việt Nam (có dấu phẩy ngăn cách).
    Ví dụ: 1500000 -> "1,500,000 VND"
    """
    return f"{amount:,} VND"


def format_date(dt: date) -> str:
    """
    Format date thành chuỗi dd/mm/yyyy
    """
    return dt.strftime("%d/%m/%Y")


def format_datetime(dt: datetime) -> str:
    """
    Format datetime thành chuỗi dd/mm/yyyy HH:MM
    """
    return dt.strftime("%d/%m/%Y %H:%M")


def days_between(start_date: date, end_date: date) -> int:
    """
    Tính số ngày giữa 2 ngày
    """
    return (end_date - start_date).days


def is_future_date(check_date: date) -> bool:
    """
    Kiểm tra ngày có phải trong tương lai không
    """
    return check_date > date.today()