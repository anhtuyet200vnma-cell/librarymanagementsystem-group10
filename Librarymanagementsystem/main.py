"""
main.py
File chính để chạy ứng dụng GUI
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from Librarymanagementsystem.ui.app import App
    
    def main():
        """Main function to start the application"""
        try:
            print("="*50)
            print("   HỆ THỐNG QUẢN LÝ THƯ VIỆN")
            print("="*50)
            print("Đang khởi động ứng dụng...")
            
            app = App()
            app.mainloop()
        except Exception as e:
            print(f"Lỗi khi khởi động ứng dụng: {e}")
            import traceback
            traceback.print_exc()
            input("\nNhấn Enter để thoát...")

    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Lỗi import: {e}")
    print("\nCách fix:")
    print("1. Đảm bảo cấu trúc thư mục đúng:")
    print("   Librarymanagementsystem/")
    print("   ├── ui/")
    print("   ├── services/")
    print("   ├── models/")
    print("   └── controllers/")
    print("\n2. Kiểm tra file __init__.py trong mỗi thư mục")
    input("\nNhấn Enter để thoát...")