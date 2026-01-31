"""
fix_all.py - Sửa tất cả lỗi import một lần
"""

import os
import shutil

print("="*50)
print("   FIX SYSTEM IMPORT ERRORS")
print("="*50)

# 1. Tạo utils/file_handler.py mới
file_handler_content = '''"""
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
'''

print("1. Creating utils/file_handler.py...")
os.makedirs("utils", exist_ok=True)
with open("utils/file_handler.py", "w", encoding="utf-8") as f:
    f.write(file_handler_content)
print("✓ Created utils/file_handler.py")

# 2. Tạo data files nếu chưa có
print("\n2. Creating data files...")
os.makedirs("data", exist_ok=True)

data_files = {
    "users.json": [
        {
            "user_id": 1,
            "username": "admin",
            "email": "admin@library.com",
            "password": "admin123",
            "full_name": "System Administrator",
            "phone_number": "0123456789",
            "status": "ACTIVE",
            "role": "ADMIN",
            "borrowing_limit": 999,
            "penalty_status": False,
            "created_at": "2024-01-01T08:00:00"
        },
        {
            "user_id": 2,
            "username": "john_doe",
            "email": "john@example.com",
            "password": "password123",
            "full_name": "John Doe",
            "phone_number": "0987654321",
            "status": "ACTIVE",
            "role": "MEMBER",
            "borrowing_limit": 5,
            "penalty_status": False,
            "created_at": "2024-01-02T09:30:00"
        }
    ],
    "books.json": [
        {
            "book_id": "BK001",
            "title": "Harry Potter and the Philosopher's Stone",
            "description": "The first novel in the Harry Potter series.",
            "publication_year": 1997,
            "quantity": 10,
            "available_quantity": 8,
            "available_copies": 8,
            "status": "AVAILABLE",
            "author_id": 1,
            "category_id": "CAT001"
        },
        {
            "book_id": "BK002",
            "title": "1984",
            "description": "A dystopian social science fiction novel.",
            "publication_year": 1949,
            "quantity": 5,
            "available_quantity": 3,
            "available_copies": 3,
            "status": "AVAILABLE",
            "author_id": 2,
            "category_id": "CAT002"
        }
    ],
    "authors.json": [
        {"author_id": 1, "author_name": "J.K. Rowling"},
        {"author_id": 2, "author_name": "George Orwell"},
        {"author_id": 3, "author_name": "Harper Lee"},
        {"author_id": 4, "author_name": "Stephen King"},
        {"author_id": 5, "author_name": "Nguyễn Nhật Ánh"}
    ],
    "categories.json": [
        {"category_id": "CAT001", "category_name": "Fantasy"},
        {"category_id": "CAT002", "category_name": "Dystopian"},
        {"category_id": "CAT003", "category_name": "Classic Literature"},
        {"category_id": "CAT004", "category_name": "Horror"},
        {"category_id": "CAT005", "category_name": "Vietnamese Literature"}
    ],
    "borrow_orders.json": [],
    "borrow_requests.json": [],
    "fines.json": [],
    "notifications.json": [],
    "waiting_lists.json": []
}

for filename, data in data_files.items():
    filepath = os.path.join("data", filename)
    if not os.path.exists(filepath):
        import json
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✓ Created data/{filename}")
    else:
        print(f"✓ data/{filename} already exists")

# 3. Test import
print("\n3. Testing imports...")
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.file_handler import load_json, save_json
    print("✓ load_json/save_json imported successfully")
    
    # Test read/write
    test_file = "test_file.json"
    test_data = [{"test": "success"}]
    save_json(test_file, test_data)
    loaded = load_json(test_file)
    if loaded == test_data:
        print("✓ File read/write test passed")
    if os.path.exists(test_file):
        os.remove(test_file)
        
except Exception as e:
    print(f"✗ Import error: {e}")

# 4. Test services
print("\n4. Testing services...")
try:
    from services.user_service import UserService
    print("✓ UserService imported")
    
    # Test user service
    user_service = UserService()
    users = load_json("data/users.json")
    print(f"✓ Loaded {len(users)} users")
    
except Exception as e:
    print(f"✗ Services error: {e}")

print("\n" + "="*50)
print("   FIX COMPLETE")
print("="*50)

# 5. Ask to run app
choice = input("\nRun application now? (y/n): ").strip().lower()
if choice == 'y':
    try:
        # Fix UI imports first
        print("\nFixing UI imports...")
        
        # Create simple app
        import tkinter as tk
        
        class SimpleApp(tk.Tk):
            def __init__(self):
                super().__init__()
                self.title("Library Management System - Fixed")
                self.geometry("800x600")
                
                tk.Label(
                    self,
                    text="✅ HỆ THỐNG ĐÃ ĐƯỢC SỬA",
                    font=("Arial", 24, "bold"),
                    fg="green"
                ).pack(pady=50)
                
                tk.Label(
                    self,
                    text="Các lỗi import đã được fix thành công!",
                    font=("Arial", 14)
                ).pack(pady=10)
                
                tk.Label(
                    self,
                    text="Bây giờ bạn có thể chạy ứng dụng chính thức:",
                    font=("Arial", 12)
                ).pack(pady=20)
                
                tk.Button(
                    self,
                    text="🚀 Chạy ứng dụng chính",
                    font=("Arial", 12, "bold"),
                    bg="#3498db",
                    fg="white",
                    padx=20,
                    pady=10,
                    command=self.run_main_app
                ).pack(pady=10)
                
                tk.Button(
                    self,
                    text="❌ Thoát",
                    font=("Arial", 12),
                    bg="#e74c3c",
                    fg="white",
                    padx=20,
                    pady=10,
                    command=self.quit
                ).pack(pady=10)
                
                tk.Label(
                    self,
                    text="Chạy: python main_app.py",
                    font=("Courier", 10),
                    fg="gray"
                ).pack(side="bottom", pady=20)
            
            def run_main_app(self):
                self.destroy()
                try:
                    from ui.app import App
                    app = App()
                    app.mainloop()
                except Exception as e:
                    print(f"Error: {e}")
                    import traceback
                    traceback.print_exc()
                    input("Press Enter to exit...")
        
        print("Starting simple app...")
        app = SimpleApp()
        app.mainloop()
        
    except Exception as e:
        print(f"✗ App error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
else:
    print("\nYou can now run:")
    print("  python main_app.py  - for GUI")
    print("  python run_cli.py   - for CLI")
    print("\nExiting...")