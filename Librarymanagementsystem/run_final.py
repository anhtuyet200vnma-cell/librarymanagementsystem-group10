"""
run_final.py - Test toàn bộ hệ thống
"""

import sys
import os

# Thêm đường dẫn
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("="*50)
print("   TEST HỆ THỐNG")
print("="*50)

# Test 1: Kiểm tra utils
print("\n1. Testing utils...")
try:
    from utils.file_handler import load_json, save_json
    print("✓ Utils imported successfully")
    
    # Test đọc/ghi file
    test_data = [{"test": "data"}]
    save_json("test.json", test_data)
    loaded = load_json("test.json")
    if loaded == test_data:
        print("✓ File read/write working")
    os.remove("test.json")
    
except Exception as e:
    print(f"✗ Utils error: {e}")

# Test 2: Kiểm tra services
print("\n2. Testing services...")
try:
    from services.user_service import UserService
    print("✓ UserService imported")
    
    from services.book_service import BookService
    print("✓ BookService imported")
    
    from services.borrow_service import BorrowService
    print("✓ BorrowService imported")
    
    from services.admin_service import AdminService
    print("✓ AdminService imported")
    
except Exception as e:
    print(f"✗ Services error: {e}")

# Test 3: Kiểm tra UI
print("\n3. Testing UI...")
try:
    from ui.auth_ui import AuthUI
    print("✓ AuthUI imported")
    
    from ui.main_ui import MainUI
    print("✓ MainUI imported")
    
    from ui.book_ui import BookUI
    print("✓ BookUI imported")
    
    from ui.admin_ui import AdminUI
    print("✓ AdminUI imported")
    
except Exception as e:
    print(f"✗ UI error: {e}")

# Test 4: Kiểm tra data files
print("\n4. Checking data files...")
data_files = [
    "data/users.json",
    "data/books.json", 
    "data/authors.json",
    "data/categories.json"
]

for file in data_files:
    if os.path.exists(file):
        print(f"✓ {file} exists")
    else:
        print(f"✗ {file} missing")
        # Tạo file trống nếu chưa có
        os.makedirs("data", exist_ok=True)
        with open(file, "w", encoding="utf-8") as f:
            f.write("[]")

# Test 5: Tạo user admin nếu chưa có
print("\n5. Creating admin user...")
try:
    from utils.file_handler import load_json, save_json
    users = load_json("data/users.json")
    
    # Kiểm tra có admin chưa
    has_admin = any(u.get("username") == "admin" for u in users)
    
    if not has_admin and users == []:
        admin_user = {
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
        }
        users.append(admin_user)
        save_json("data/users.json", users)
        print("✓ Admin user created")
    elif has_admin:
        print("✓ Admin user already exists")
    else:
        print("✓ Users file populated")
        
except Exception as e:
    print(f"✗ Error creating admin: {e}")

print("\n" + "="*50)
print("   TEST COMPLETE")
print("="*50)

# Hỏi có chạy app không
choice = input("\nRun application? (y/n): ").strip().lower()
if choice == 'y':
    try:
        from ui.app import App
        print("\nStarting application...")
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"\n✗ Application error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
else:
    print("\nExiting...")