"""
file_handler.py
Xử lý đọc/ghi file JSON cho toàn bộ hệ thống
"""

import json
import os


# ===== CÁC HÀM CHÍNH =====
def load_json(file_path):
    """
    Đọc file JSON và trả về dữ liệu (List/Dict).
    Nếu file không tồn tại hoặc lỗi, trả về danh sách rỗng [].
    """
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content: 
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[Error] Lỗi đọc file {file_path}: {e}")
        return []


def save_json(file_path, data):
    """
    Ghi dữ liệu xuống file JSON.
    Tự động tạo thư mục nếu chưa có.
    """
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"[Error] Lỗi ghi file {file_path}: {e}")
        return False


def check_file_exists(file_path):
    """Kiểm tra file có tồn tại không"""
    return os.path.exists(file_path)


def create_file_if_not_exists(file_path, default_data=None):
    """Tạo file nếu chưa tồn tại"""
    if not os.path.exists(file_path):
        save_json(file_path, default_data or [])
        return True
    return False


# ===== CLASS WRAPPER (cho tương thích) =====
class FileHandler:
    """Class wrapper cho tương thích với code cũ"""
    
    @staticmethod
    def read_json(file_path):
        return load_json(file_path)
    
    @staticmethod
    def write_json(file_path, data):
        return save_json(file_path, data)
    
    @staticmethod
    def load_json(file_path):
        return load_json(file_path)
    
    @staticmethod
    def save_json(file_path, data):
        return save_json(file_path, data)
    
    @staticmethod
    def check_file_exists(file_path):
        return check_file_exists(file_path)
    
    @staticmethod
    def create_file_if_not_exists(file_path, default_data=None):
        return create_file_if_not_exists(file_path, default_data)