import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from services.admin_service import AdminService
from services.borrow_service import BorrowService  # THÊM DÒNG NÀY

class AdminUI(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.admin_service = AdminService()
        self.borrow_service = BorrowService()  # THÊM DÒNG NÀY
        
        self.build_ui()

    def build_ui(self):
        self.configure(bg="white")
        
        # Header
        tk.Button(
            self,
            text="⬅ Quay lại",
            width=12,
            font=("Arial", 10),
            bg="#7f8c8d",
            fg="white",
            command=lambda: self.app.show("main")
        ).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            self, 
            text="QUẢN TRỊ HỆ THỐNG", 
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=10)

        # Create notebook (tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, padx=20, fill="both", expand=True)

        # Tab 1: Thêm sách
        add_book_frame = tk.Frame(notebook, bg="white")
        notebook.add(add_book_frame, text="📚 Thêm sách")
        self.build_add_book_tab(add_book_frame)

        # Tab 2: Quản lý sách
        manage_book_frame = tk.Frame(notebook, bg="white")
        notebook.add(manage_book_frame, text="📖 Quản lý sách")
        self.build_manage_book_tab(manage_book_frame)

        # Tab 3: Quản lý người dùng
        manage_user_frame = tk.Frame(notebook, bg="white")
        notebook.add(manage_user_frame, text="👥 Quản lý người dùng")
        self.build_manage_user_tab(manage_user_frame)

        # Tab 4: Thống kê
        stats_frame = tk.Frame(notebook, bg="white")
        notebook.add(stats_frame, text="📊 Thống kê")
        self.build_stats_tab(stats_frame)

        # Tab 5: QUẢN LÝ MƯỢN TRẢ & PHẠT (TAB MỚI)
        borrow_fine_frame = tk.Frame(notebook, bg="white")
        notebook.add(borrow_fine_frame, text="💰 Quản lý mượn trả & phạt")
        self.build_borrow_fine_tab(borrow_fine_frame)

    # ===== CÁC HÀM TAB CŨ (GIỮ NGUYÊN) =====
    
    def build_add_book_tab(self, parent):
        """Build add book tab"""
        # Form container
        form_frame = tk.Frame(parent, bg="white", padx=20, pady=20)
        form_frame.pack()

        # Book ID
        tk.Label(
            form_frame, 
            text="Mã sách (Book ID):", 
            font=("Arial", 11),
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=8)
        
        self.book_id_entry = tk.Entry(
            form_frame, 
            width=30,
            font=("Arial", 11),
            relief="solid"
        )
        self.book_id_entry.grid(row=0, column=1, pady=8, padx=(10, 0))

        # Title
        tk.Label(
            form_frame, 
            text="Tiêu đề:", 
            font=("Arial", 11),
            bg="white"
        ).grid(row=1, column=0, sticky="w", pady=8)
        
        self.title_entry = tk.Entry(
            form_frame, 
            width=30,
            font=("Arial", 11),
            relief="solid"
        )
        self.title_entry.grid(row=1, column=1, pady=8, padx=(10, 0))

        # Author ID
        tk.Label(
            form_frame, 
            text="Mã tác giả:", 
            font=("Arial", 11),
            bg="white"
        ).grid(row=2, column=0, sticky="w", pady=8)
        
        self.author_id_entry = tk.Entry(
            form_frame, 
            width=30,
            font=("Arial", 11),
            relief="solid"
        )
        self.author_id_entry.grid(row=2, column=1, pady=8, padx=(10, 0))
        self.author_id_entry.insert(0, "1")

        # Category ID
        tk.Label(
            form_frame, 
            text="Mã thể loại:", 
            font=("Arial", 11),
            bg="white"
        ).grid(row=3, column=0, sticky="w", pady=8)
        
        self.category_id_entry = tk.Entry(
            form_frame, 
            width=30,
            font=("Arial", 11),
            relief="solid"
        )
        self.category_id_entry.grid(row=3, column=1, pady=8, padx=(10, 0))
        self.category_id_entry.insert(0, "CAT001")

        # Quantity
        tk.Label(
            form_frame, 
            text="Số lượng:", 
            font=("Arial", 11),
            bg="white"
        ).grid(row=4, column=0, sticky="w", pady=8)
        
        self.quantity_entry = tk.Entry(
            form_frame, 
            width=30,
            font=("Arial", 11),
            relief="solid"
        )
        self.quantity_entry.grid(row=4, column=1, pady=8, padx=(10, 0))
        self.quantity_entry.insert(0, "10")

        # Year
        tk.Label(
            form_frame, 
            text="Năm xuất bản:", 
            font=("Arial", 11),
            bg="white"
        ).grid(row=5, column=0, sticky="w", pady=8)
        
        self.year_entry = tk.Entry(
            form_frame, 
            width=30,
            font=("Arial", 11),
            relief="solid"
        )
        self.year_entry.grid(row=5, column=1, pady=8, padx=(10, 0))
        self.year_entry.insert(0, "2024")

        # Description
        tk.Label(
            form_frame, 
            text="Mô tả:", 
            font=("Arial", 11),
            bg="white"
        ).grid(row=6, column=0, sticky="nw", pady=8)
        
        self.description_text = tk.Text(
            form_frame, 
            width=30,
            height=4,
            font=("Arial", 11),
            relief="solid"
        )
        self.description_text.grid(row=6, column=1, pady=8, padx=(10, 0))
        self.description_text.insert("1.0", "Mô tả sách")

        # Add button
        tk.Button(
            form_frame,
            text="THÊM SÁCH",
            width=20,
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            relief="raised",
            padx=10,
            pady=5,
            command=self.add_book
        ).grid(row=7, column=1, sticky="w", pady=20, padx=(10, 0))

        # Info label
        self.add_book_info = tk.Label(
            form_frame,
            text="",
            font=("Arial", 10),
            bg="white",
            fg="#27ae60"
        )
        self.add_book_info.grid(row=8, column=0, columnspan=2, pady=10)

    def build_manage_book_tab(self, parent):
        """Build manage book tab"""
        # Search frame
        search_frame = tk.Frame(parent, bg="white", padx=20, pady=10)
        search_frame.pack(fill="x")

        tk.Label(
            search_frame, 
            text="Tìm sách (ID hoặc tên):", 
            font=("Arial", 11),
            bg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.search_book_entry = tk.Entry(
            search_frame, 
            width=25,
            font=("Arial", 11),
            relief="solid"
        )
        self.search_book_entry.pack(side="left", padx=(0, 10))
        
        tk.Button(
            search_frame,
            text="🔍 Tìm",
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            command=self.search_books_admin
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            search_frame,
            text="🗑 Xóa sách đã chọn",
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            command=self.delete_selected_book
        ).pack(side="right")

        # Table frame
        table_frame = tk.Frame(parent, bg="white")
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Create Treeview
        columns = ("Mã sách", "Tiêu đề", "Tác giả", "Thể loại", "Số lượng", "Có sẵn", "Trạng thái")
        self.books_tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings",
            height=12,
            selectmode="browse"
        )

        # Define headings
        column_widths = [100, 250, 120, 100, 80, 80, 100]
        for col, width in zip(columns, column_widths):
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=width, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.books_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.books_tree.configure(yscrollcommand=scrollbar.set)
        
        self.books_tree.pack(side="left", fill="both", expand=True)

        # Load books on tab open
        self.load_all_books()

    def build_manage_user_tab(self, parent):
        """Build manage user tab"""
        # Search frame
        search_frame = tk.Frame(parent, bg="white", padx=20, pady=10)
        search_frame.pack(fill="x")

        tk.Label(
            search_frame, 
            text="Tìm người dùng:", 
            font=("Arial", 11),
            bg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.search_user_entry = tk.Entry(
            search_frame, 
            width=25,
            font=("Arial", 11),
            relief="solid"
        )
        self.search_user_entry.pack(side="left", padx=(0, 10))
        
        tk.Button(
            search_frame,
            text="🔍 Tìm",
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            command=self.search_users
        ).pack(side="left")

        # Table frame
        table_frame = tk.Frame(parent, bg="white")
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Create Treeview
        columns = ("ID", "Username", "Họ tên", "Email", "Vai trò", "Trạng thái", "Giới hạn mượn")
        self.users_tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings",
            height=10
        )

        # Define headings
        column_widths = [50, 100, 150, 180, 80, 100, 100]
        for col, width in zip(columns, column_widths):
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=width, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.users_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side="left", fill="both", expand=True)

        # Control frame
        control_frame = tk.Frame(parent, bg="white", padx=20, pady=10)
        control_frame.pack(fill="x")

        tk.Label(
            control_frame, 
            text="Thay đổi trạng thái:", 
            font=("Arial", 11),
            bg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.status_var = tk.StringVar(value="ACTIVE")
        status_menu = tk.OptionMenu(
            control_frame, 
            self.status_var, 
            "ACTIVE", "INACTIVE", "SUSPENDED"
        )
        status_menu.pack(side="left", padx=(0, 10))
        
        tk.Button(
            control_frame,
            text="Cập nhật trạng thái",
            font=("Arial", 10),
            bg="#f39c12",
            fg="white",
            command=self.update_user_status
        ).pack(side="left")

        # Load users
        self.load_all_users()

    def build_stats_tab(self, parent):
        """Build statistics tab"""
        stats_frame = tk.Frame(parent, bg="white", padx=20, pady=20)
        stats_frame.pack()

        # Stats display
        self.stats_text = tk.Text(
            stats_frame,
            width=50,
            height=15,
            font=("Courier", 10),
            relief="solid",
            bg="#f8f9fa"
        )
        self.stats_text.pack(pady=10)

        # Refresh button
        tk.Button(
            stats_frame,
            text="🔄 Làm mới thống kê",
            font=("Arial", 11),
            bg="#9b59b6",
            fg="white",
            command=self.refresh_stats
        ).pack(pady=10)

        # Load initial stats
        self.refresh_stats()

    # ===== CÁC HÀM TAB MƯỢN TRẢ & PHẠT MỚI =====

    def build_borrow_fine_tab(self, parent):
        """Tab mới: Quản lý mượn trả và phạt"""
        # Container chính
        main_frame = tk.Frame(parent, bg="white", padx=20, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Phần trên: Tìm kiếm đơn mượn
        search_frame = tk.Frame(main_frame, bg="white", pady=10)
        search_frame.pack(fill="x")

        tk.Label(
            search_frame,
            text="Tìm đơn mượn:",
            font=("Arial", 11),
            bg="white"
        ).pack(side="left", padx=(0, 10))

        # Ô nhập Borrow ID
        tk.Label(
            search_frame,
            text="Borrow ID:",
            font=("Arial", 10),
            bg="white"
        ).pack(side="left", padx=(0, 5))
        
        self.admin_borrow_id_entry = tk.Entry(
            search_frame,
            width=25,
            font=("Arial", 10),
            relief="solid"
        )
        self.admin_borrow_id_entry.pack(side="left", padx=(0, 10))

        # Ô nhập User ID
        tk.Label(
            search_frame,
            text="User ID:",
            font=("Arial", 10),
            bg="white"
        ).pack(side="left", padx=(0, 5))
        
        self.admin_user_id_entry = tk.Entry(
            search_frame,
            width=15,
            font=("Arial", 10),
            relief="solid"
        )
        self.admin_user_id_entry.pack(side="left", padx=(0, 10))

        # Nút tìm kiếm
        tk.Button(
            search_frame,
            text="🔍 Tìm",
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            command=self.search_borrow_admin
        ).pack(side="left", padx=(0, 10))

        # Nút xem tất cả
        tk.Button(
            search_frame,
            text="📋 Tất cả đơn mượn",
            font=("Arial", 10),
            bg="#9b59b6",
            fg="white",
            command=self.show_all_borrows
        ).pack(side="left")

        # Bảng hiển thị đơn mượn
        table_frame = tk.Frame(main_frame, bg="white", pady=10)
        table_frame.pack(fill="both", expand=True)

        # Treeview
        columns = ("Mã mượn", "User ID", "Book ID", "Ngày mượn", "Hạn trả", "Trạng thái", "Phạt (VND)")
        self.admin_borrows_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        column_widths = [120, 70, 100, 100, 100, 90, 100]
        for col, width in zip(columns, column_widths):
            self.admin_borrows_tree.heading(col, text=col)
            self.admin_borrows_tree.column(col, width=width, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.admin_borrows_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.admin_borrows_tree.configure(yscrollcommand=scrollbar.set)
        self.admin_borrows_tree.pack(side="left", fill="both", expand=True)

        # Phần dưới: Thao tác với đơn mượn đã chọn
        action_frame = tk.Frame(main_frame, bg="white", pady=15)
        action_frame.pack(fill="x")

        # Tình trạng sách
        tk.Label(
            action_frame,
            text="Tình trạng sách:",
            font=("Arial", 11),
            bg="white"
        ).pack(side="left", padx=(0, 10))

        self.admin_condition_var = tk.StringVar(value="GOOD")
        condition_menu = tk.OptionMenu(
            action_frame,
            self.admin_condition_var,
            "GOOD", "DAMAGED", "TORN", "LOST"
        )
        condition_menu.config(width=8)
        condition_menu.pack(side="left", padx=(0, 20))

        # Ngày thực tế (tùy chọn)
        tk.Label(
            action_frame,
            text="Ngày mượn thực:",
            font=("Arial", 10),
            bg="white"
        ).pack(side="left", padx=(0, 5))
        
        self.admin_actual_borrow_entry = tk.Entry(
            action_frame,
            width=12,
            font=("Arial", 10),
            relief="solid"
        )
        self.admin_actual_borrow_entry.pack(side="left", padx=(0, 10))
        self.admin_actual_borrow_entry.insert(0, "")

        tk.Label(
            action_frame,
            text="Ngày trả thực:",
            font=("Arial", 10),
            bg="white"
        ).pack(side="left", padx=(0, 5))
        
        self.admin_actual_return_entry = tk.Entry(
            action_frame,
            width=12,
            font=("Arial", 10),
            relief="solid"
        )
        self.admin_actual_return_entry.pack(side="left", padx=(0, 10))
        self.admin_actual_return_entry.insert(0, "")

        # Các nút thao tác
        button_frame = tk.Frame(action_frame, bg="white")
        button_frame.pack(side="left", padx=(20, 0))

        # Nút trả sách có tính phạt
        tk.Button(
            button_frame,
            text="📚 TRẢ SÁCH (TÍNH PHẠT)",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            width=20,
            command=self.admin_return_with_fine
        ).pack(side="left", padx=(0, 10))

        # Nút trả sách không phạt (cho admin)
        tk.Button(
            button_frame,
            text="📚 TRẢ SÁCH (KHÔNG PHẠT)",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            width=20,
            command=self.admin_return_no_fine
        ).pack(side="left", padx=(0, 10))

        # Nút làm mới
        tk.Button(
            button_frame,
            text="🔄 Làm mới",
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            command=self.show_all_borrows
        ).pack(side="left")

        # Ghi chú
        note_label = tk.Label(
            main_frame,
            text="📝 Ghi chú: Admin có thể trả sách không tính phạt (miễn phí) hoặc tính phạt theo quy định",
            font=("Arial", 9, "italic"),
            bg="white",
            fg="#7f8c8d"
        )
        note_label.pack(pady=5)
    # ===== THÊM HÀM XÓA DỮ LIỆU CHO ADMIN =====
    def clear_admin_borrow_data(self):
        """Xóa tất cả dữ liệu nhập trong tab quản lý mượn trả"""
        self.admin_borrow_id_entry.delete(0, tk.END)
        self.admin_user_id_entry.delete(0, tk.END)
        self.admin_actual_borrow_entry.delete(0, tk.END)
        self.admin_actual_return_entry.delete(0, tk.END)
        self.admin_condition_var.set("GOOD")
        # Xóa dữ liệu trong tree
        for item in self.admin_borrows_tree.get_children():
            self.admin_borrows_tree.delete(item)
        # Thêm hàng thông báo
        self.admin_borrows_tree.insert("", "end", values=("Đã xóa dữ liệu tìm kiếm", "", "", "", "", "", ""))
        # Load tất cả đơn mượn ban đầu
        self.show_all_borrows()

    def search_borrow_admin(self):
        """Tìm kiếm đơn mượn trong admin"""
        borrow_id = self.admin_borrow_id_entry.get().strip()
        user_id = self.admin_user_id_entry.get().strip()

        try:
            # Clear tree
            for item in self.admin_borrows_tree.get_children():
                self.admin_borrows_tree.delete(item)

            # Get all borrows
            all_borrows = self.borrow_service.get_user_borrows(0)  # 0 = get all

            if not all_borrows:
                self.admin_borrows_tree.insert("", "end", values=("Không có dữ liệu", "", "", "", "", "", ""))
                return

            # Filter
            filtered_borrows = []
            for borrow in all_borrows:
                match_borrow_id = not borrow_id or borrow_id in borrow.get("borrow_id", "")
                match_user_id = not user_id or user_id == str(borrow.get("user_id", ""))
                
                if match_borrow_id and match_user_id:
                    filtered_borrows.append(borrow)

            # Display
            if not filtered_borrows:
                self.admin_borrows_tree.insert("", "end", values=("Không tìm thấy", "", "", "", "", "", ""))
                return

            for borrow in filtered_borrows:
                status_text = {
                    "BORROWED": "Đang mượn",
                    "RETURNED": "Đã trả",
                    "OVERDUE": "Quá hạn"
                }.get(borrow.get("status", ""), borrow.get("status", ""))

                fine_amount = borrow.get("fine_amount", 0)
                fine_text = f"{fine_amount:,}" if fine_amount > 0 else "0"

                self.admin_borrows_tree.insert("", "end", values=(
                    borrow.get("borrow_id", ""),
                    borrow.get("user_id", ""),
                    borrow.get("book_id", ""),
                    borrow.get("borrow_date", "")[:10] if borrow.get("borrow_date") else "",
                    borrow.get("due_date", "")[:10] if borrow.get("due_date") else "",
                    status_text,
                    fine_text
                ))

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tìm kiếm: {str(e)}")

    def show_all_borrows(self):
        """Hiển thị tất cả đơn mượn"""
        try:
            # Clear tree
            for item in self.admin_borrows_tree.get_children():
                self.admin_borrows_tree.delete(item)

            # Get all borrows
            all_borrows = self.borrow_service.get_user_borrows(0)  # 0 = get all

            if not all_borrows:
                self.admin_borrows_tree.insert("", "end", values=("Không có dữ liệu", "", "", "", "", "", ""))
                return

            # Display all
            for borrow in all_borrows:
                status_text = {
                    "BORROWED": "Đang mượn",
                    "RETURNED": "Đã trả",
                    "OVERDUE": "Quá hạn"
                }.get(borrow.get("status", ""), borrow.get("status", ""))

                fine_amount = borrow.get("fine_amount", 0)
                fine_text = f"{fine_amount:,}" if fine_amount > 0 else "0"

                self.admin_borrows_tree.insert("", "end", values=(
                    borrow.get("borrow_id", ""),
                    borrow.get("user_id", ""),
                    borrow.get("book_id", ""),
                    borrow.get("borrow_date", "")[:10] if borrow.get("borrow_date") else "",
                    borrow.get("due_date", "")[:10] if borrow.get("due_date") else "",
                    status_text,
                    fine_text
                ))

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải dữ liệu: {str(e)}")

    def admin_return_with_fine(self):
        """Admin trả sách có tính phạt"""
        selected_item = self.admin_borrows_tree.selection()
        if not selected_item:
            messagebox.showwarning("Thông báo", "Vui lòng chọn đơn mượn cần trả.")
            return

        values = self.admin_borrows_tree.item(selected_item[0], "values")
        borrow_id = values[0]
        
        # Kiểm tra trạng thái
        status = values[5]
        if status == "Đã trả":
            messagebox.showwarning("Thông báo", "Sách đã được trả trước đó.")
            return

        condition = self.admin_condition_var.get()
        actual_borrow_date = self.admin_actual_borrow_entry.get().strip()
        actual_return_date = self.admin_actual_return_entry.get().strip()

        confirm = messagebox.askyesno(
            "Xác nhận trả sách",
            f"Trả sách với tình trạng: {condition}\n"
            f"Borrow ID: {borrow_id}\n\n"
            f"Hệ thống sẽ tự tính phạt dựa trên tình trạng và ngày thực tế."
        )

        if confirm:
            try:
                result = self.borrow_service.return_book_with_fine(
                    borrow_id=borrow_id,
                    condition=condition,
                    actual_borrow_date=actual_borrow_date if actual_borrow_date else None,
                    actual_return_date=actual_return_date if actual_return_date else None
                )

                if result.get("success"):
                    # Hiển thị thông báo chi tiết
                    messagebox.showinfo("KẾT QUẢ TRẢ SÁCH", result.get("message"))
                    
                    # Clear inputs
                    self.admin_actual_borrow_entry.delete(0, tk.END)
                    self.admin_actual_return_entry.delete(0, tk.END)
                    
                    # Refresh danh sách
                    self.show_all_borrows()
                    
                    # Refresh thống kê
                    self.refresh_stats()
                else:
                    messagebox.showerror("Lỗi", result.get("message"))

            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Lỗi: {str(e)}")

    def admin_return_no_fine(self):
        """Admin trả sách không tính phạt (miễn phí)"""
        selected_item = self.admin_borrows_tree.selection()
        if not selected_item:
            messagebox.showwarning("Thông báo", "Vui lòng chọn đơn mượn cần trả.")
            return

        values = self.admin_borrows_tree.item(selected_item[0], "values")
        borrow_id = values[0]
        
        # Kiểm tra trạng thái
        status = values[5]
        if status == "Đã trả":
            messagebox.showwarning("Thông báo", "Sách đã được trả trước đó.")
            return

        confirm = messagebox.askyesno(
            "Xác nhận trả sách (MIỄN PHẠT)",
            f"Bạn đang trả sách MIỄN PHẠT cho:\nBorrow ID: {borrow_id}\n\n"
            f"Đây là quyền đặc biệt của Admin. Chỉ sử dụng trong trường hợp đặc biệt."
        )

        if confirm:
            try:
                result = self.borrow_service.return_book(borrow_id)

                if result.get("success"):
                    messagebox.showinfo("Thành công", "✅ Đã trả sách thành công (miễn phạt).")
                    
                    # Refresh danh sách
                    self.show_all_borrows()
                    
                    # Refresh thống kê
                    self.refresh_stats()
                else:
                    messagebox.showerror("Lỗi", result.get("message"))

            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Lỗi: {str(e)}")

    # ===== CÁC HÀM CŨ GIỮ NGUYÊN =====

    def add_book(self):
        """Handle add book action"""
        book_id = self.book_id_entry.get().strip()
        title = self.title_entry.get().strip()
        author_id = self.author_id_entry.get().strip()
        category_id = self.category_id_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        year = self.year_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()

        # Validate
        if not all([book_id, title, author_id, category_id, quantity, year]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showwarning("Sai định dạng", "Số lượng phải là số dương.")
            return

        if not year.isdigit() or int(year) < 1000 or int(year) > 2100:
            messagebox.showwarning("Sai định dạng", "Năm xuất bản không hợp lệ.")
            return

        try:
            # Prepare book data
            book_data = {
                "book_id": book_id,
                "title": title,
                "description": description,
                "publication_year": int(year),
                "quantity": int(quantity),
                "available_quantity": int(quantity),
                "available_copies": int(quantity),
                "status": "AVAILABLE",
                "author_id": int(author_id) if author_id.isdigit() else author_id,
                "category_id": category_id
            }

            success = self.admin_service.add_book(book_data)
            if success:
                messagebox.showinfo("Thành công", f"Đã thêm sách '{title}' thành công.")
                self.add_book_info.config(text=f"Đã thêm sách: {title}", fg="#27ae60")
                
                # Clear form
                self.book_id_entry.delete(0, tk.END)
                self.title_entry.delete(0, tk.END)
                self.description_text.delete("1.0", tk.END)
                self.book_id_entry.focus()
                
                # Refresh books list
                self.load_all_books()
            else:
                messagebox.showerror("Lỗi", "Không thể thêm sách. Có thể Book ID đã tồn tại.")
                self.add_book_info.config(text="Lỗi khi thêm sách", fg="#e74c3c")
                
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Lỗi: {str(e)}")
            self.add_book_info.config(text=f"Lỗi: {str(e)}", fg="#e74c3c")

    def load_all_books(self):
        """Load all books for management"""
        try:
            # Clear existing items
            for item in self.books_tree.get_children():
                self.books_tree.delete(item)

            # Get all books from service
            all_books = self.admin_service.get_all_books()
            
            if not all_books:
                self.books_tree.insert("", "end", values=("Không có sách", "", "", "", "", "", ""))
                return

            # Insert books into table - FIX HIỂN THỊ AN TOÀN
            for book in all_books:
                # Lấy tên tác giả (kiểm tra an toàn)
                author_name = "Unknown"
                if isinstance(book.get("author_name"), str):
                    author_name = book.get("author_name", "Unknown")
                elif isinstance(book.get("author_id"), (int, str)):
                    author_name = f"Tác giả {book.get('author_id')}"
                
                # Lấy tên thể loại (kiểm tra an toàn)
                category_name = "Unknown"
                if isinstance(book.get("category_name"), str):
                    category_name = book.get("category_name", "Unknown")
                elif isinstance(book.get("category_id"), str):
                    category_name = book.get("category_id", "Unknown")
                
                # Trạng thái
                status_text = "Có sẵn" if book.get("status") == "AVAILABLE" else "Đã hết"
                
                # Hiển thị
                self.books_tree.insert("", "end", values=(
                    book.get("book_id", ""),
                    book.get("title", "")[:35],  # Cắt ngắn nếu dài
                    author_name[:20],  # Cắt ngắn
                    category_name[:15],  # Cắt ngắn
                    book.get("quantity", 0),
                    book.get("available_quantity", 0),
                    status_text
                ))
                
        except Exception as e:
            print(f"⚠️ Lỗi nhẹ khi tải sách: {e}")
            self.books_tree.insert("", "end", values=("Lỗi tải", f"Chi tiết: {str(e)[:30]}", "", "", "", "", ""))

    def search_books_admin(self):
        """Search books in admin tab"""
        keyword = self.search_book_entry.get().strip().lower()
        
        if not keyword:
            self.load_all_books()
            return
        
        try:
            # Clear existing items
            for item in self.books_tree.get_children():
                self.books_tree.delete(item)

            # Get search results
            search_results = []
            all_books = self.admin_service.get_all_books()
            
            for book in all_books:
                if (keyword in book.get("book_id", "").lower() or 
                    keyword in book.get("title", "").lower() or
                    keyword in str(book.get("author_id", "")).lower() or
                    keyword in book.get("category_id", "").lower() or
                    keyword in book.get("author_name", "").lower() or
                    keyword in book.get("category_name", "").lower()):
                    search_results.append(book)

            # Display results
            if not search_results:
                self.books_tree.insert("", "end", values=("Không tìm thấy", "", "", "", "", "", ""))
                return
                
            for book in search_results:
                # Lấy tên tác giả (kiểm tra an toàn)
                author_name = "Unknown"
                if isinstance(book.get("author_name"), str):
                    author_name = book.get("author_name", "Unknown")
                elif isinstance(book.get("author_id"), (int, str)):
                    author_name = f"Tác giả {book.get('author_id')}"
                
                # Lấy tên thể loại (kiểm tra an toàn)
                category_name = "Unknown"
                if isinstance(book.get("category_name"), str):
                    category_name = book.get("category_name", "Unknown")
                elif isinstance(book.get("category_id"), str):
                    category_name = book.get("category_id", "Unknown")
                
                # Trạng thái
                status_text = "Có sẵn" if book.get("status") == "AVAILABLE" else "Đã hết"
                
                self.books_tree.insert("", "end", values=(
                    book.get("book_id", ""),
                    book.get("title", "")[:35],
                    author_name[:20],
                    category_name[:15],
                    book.get("quantity", 0),
                    book.get("available_quantity", 0),
                    status_text
                ))
        except Exception as e:
            print(f"Error searching books: {e}")
            self.books_tree.insert("", "end", values=("Lỗi tìm kiếm", f"{str(e)[:30]}", "", "", "", "", ""))

    def delete_selected_book(self):
        """Delete selected book"""
        selected_item = self.books_tree.selection()
        if not selected_item:
            messagebox.showwarning("Thông báo", "Vui lòng chọn sách cần xóa.")
            return
        
        values = self.books_tree.item(selected_item[0], "values")
        book_id = values[0]
        book_title = values[1]

        confirm = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa sách:\n'{book_title}' (ID: {book_id})?"
        )
        
        if confirm:
            try:
                success = self.admin_service.delete_book(book_id)
                if success:
                    messagebox.showinfo("Thành công", f"Đã xóa sách '{book_title}'.")
                    self.load_all_books()
                else:
                    messagebox.showerror("Lỗi", "Không thể xóa sách. Có thể sách đang được mượn.")
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Lỗi: {str(e)}")

    def load_all_users(self):
        """Load all users for management"""
        try:
            # Clear existing items
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)

            # Get all users from service
            all_users = self.admin_service.get_all_users()
            
            if not all_users:
                self.users_tree.insert("", "end", values=("Không có dữ liệu", "", "", "", "", "", ""))
                return

            # Insert users into table
            for user in all_users:
                role_text = {
                    "ADMIN": "Quản trị",
                    "MEMBER": "Thành viên"
                }.get(user.get("role", ""), user.get("role", ""))

                status_text = {
                    "ACTIVE": "Hoạt động",
                    "INACTIVE": "Không hoạt động",
                    "SUSPENDED": "Tạm khóa"
                }.get(user.get("status", ""), user.get("status", ""))

                self.users_tree.insert("", "end", values=(
                    user.get("user_id", ""),
                    user.get("username", ""),
                    user.get("full_name", ""),
                    user.get("email", ""),
                    role_text,
                    status_text,
                    user.get("borrowing_limit", 5)
                ))
        except Exception as e:
            print(f"Error loading users: {e}")

    def search_users(self):
        """Search users in admin tab"""
        keyword = self.search_user_entry.get().strip().lower()
        
        if not keyword:
            self.load_all_users()
            return
        
        try:
            # Clear existing items
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)

            # Get search results
            search_results = self.admin_service.search_users(keyword)
            
            if not search_results:
                self.users_tree.insert("", "end", values=("Không tìm thấy", "", "", "", "", "", ""))
                return

            # Display results
            for user in search_results:
                role_text = {
                    "ADMIN": "Quản trị",
                    "MEMBER": "Thành viên"
                }.get(user.get("role", ""), user.get("role", ""))

                status_text = {
                    "ACTIVE": "Hoạt động",
                    "INACTIVE": "Không hoạt động",
                    "SUSPENDED": "Tạm khóa"
                }.get(user.get("status", ""), user.get("status", ""))

                self.users_tree.insert("", "end", values=(
                    user.get("user_id", ""),
                    user.get("username", ""),
                    user.get("full_name", ""),
                    user.get("email", ""),
                    role_text,
                    status_text,
                    user.get("borrowing_limit", 5)
                ))
        except Exception as e:
            print(f"Error searching users: {e}")

    def update_user_status(self):
        """Update selected user's status"""
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("Thông báo", "Vui lòng chọn người dùng cần cập nhật.")
            return
        
        values = self.users_tree.item(selected_item[0], "values")
        user_id = values[0]
        username = values[1]
        new_status = self.status_var.get()

        confirm = messagebox.askyesno(
            "Xác nhận cập nhật",
            f"Bạn có chắc chắn muốn thay đổi trạng thái của '{username}' (ID: {user_id}) thành '{new_status}'?"
        )
        
        if confirm:
            try:
                success = self.admin_service.manage_user_status(int(user_id), new_status)
                if success:
                    messagebox.showinfo("Thành công", f"Đã cập nhật trạng thái của '{username}'.")
                    self.load_all_users()
                else:
                    messagebox.showerror("Lỗi", "Không thể cập nhật trạng thái.")
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Lỗi: {str(e)}")

    def refresh_stats(self):
        """Refresh system statistics"""
        try:
            stats = self.admin_service.get_system_stats()
            
            self.stats_text.delete("1.0", tk.END)
            
            stats_text = f"""
{'='*50}
            THỐNG KÊ HỆ THỐNG
{'='*50}

SÁCH:
• Tổng số sách: {stats.get('total_books', 0):,}
• Sách có sẵn: {stats.get('available_books', 0):,}
• Sách đang được mượn: {stats.get('active_borrows', 0):,}

NGƯỜI DÙNG:
• Tổng số người dùng: {stats.get('total_users', 0):,}
• Thành viên: {stats.get('member_count', 0):,}
• Quản trị viên: {stats.get('admin_count', 0):,}

HOẠT ĐỘNG:
• Đang mượn: {stats.get('active_borrows', 0):,}
• Đã trả: {stats.get('returned_borrows', 0):,}
• Quá hạn: {stats.get('overdue_borrows', 0):,}

TIỀN PHẠT:
• Tổng tiền phạt: {stats.get('total_fines', 0):,} VND
• Chưa thanh toán: {stats.get('unpaid_fines', 0):,} VND
• Đã thanh toán: {stats.get('paid_fines', 0):,} VND

{'='*50}
            CẬP NHẬT: {stats.get('last_updated', 'N/A')}
{'='*50}
"""
            self.stats_text.insert("1.0", stats_text)
            
        except Exception as e:
            self.stats_text.delete("1.0", tk.END)
            self.stats_text.insert("1.0", f"Lỗi khi tải thống kê: {str(e)}")