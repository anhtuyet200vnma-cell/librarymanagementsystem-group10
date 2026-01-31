import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from services.borrow_service import BorrowService

class BorrowUI(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.borrow_service = BorrowService()
        
        # Cấu hình font mặc định
        self.title_font = ("Arial", 22, "bold")
        self.label_font = ("Arial", 11)
        self.small_font = ("Arial", 9)
        self.entry_font = ("Arial", 10)
        self.button_font = ("Arial", 11, "bold")
        
        self.build_ui()

    def build_ui(self):
        self.configure(bg="white")
        
        # Header
        tk.Button(
            self,
            text="⬅ Quay lại",
            width=12,
            font=self.entry_font,
            bg="#7f8c8d",
            fg="white",
            command=lambda: self.app.show("main")
        ).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            self, 
            text="QUẢN LÝ MƯỢN TRẢ SÁCH", 
            font=self.title_font,
            bg="white",
            fg="#2c3e50"
        ).pack(pady=10)

        # Create notebook (tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, padx=20, fill="both", expand=True)

        # Tab 1: Mượn sách
        borrow_frame = tk.Frame(notebook, bg="white")
        notebook.add(borrow_frame, text="📚 Mượn sách")
        self.build_borrow_tab(borrow_frame)

        # Tab 2: Trả sách
        return_frame = tk.Frame(notebook, bg="white")
        notebook.add(return_frame, text="📖 Trả sách")
        self.build_return_tab(return_frame)

        # Tab 3: Lịch sử mượn
        history_frame = tk.Frame(notebook, bg="white")
        notebook.add(history_frame, text="📋 Lịch sử")
        self.build_history_tab(history_frame)

    def build_borrow_tab(self, parent):
        """Build borrow tab"""
        # Form container
        form_frame = tk.Frame(parent, bg="white", padx=30, pady=25)
        form_frame.pack()

        # User ID
        tk.Label(
            form_frame, 
            text="User ID:", 
            font=self.label_font,
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=12)
        
        self.borrow_user_entry = tk.Entry(
            form_frame, 
            width=32,
            font=self.entry_font,
            relief="solid",
            bd=1
        )
        self.borrow_user_entry.grid(row=0, column=1, pady=12, padx=(15, 0))

        # Book ID
        tk.Label(
            form_frame, 
            text="Book ID:", 
            font=self.label_font,
            bg="white"
        ).grid(row=1, column=0, sticky="w", pady=12)
        
        self.borrow_book_entry = tk.Entry(
            form_frame, 
            width=32,
            font=self.entry_font,
            relief="solid",
            bd=1
        )
        self.borrow_book_entry.grid(row=1, column=1, pady=12, padx=(15, 0))

        # Borrow button
        tk.Button(
            form_frame,
            text="MƯỢN SÁCH",
            width=20,
            font=self.button_font,
            bg="#2ecc71",
            fg="white",
            relief="raised",
            bd=2,
            padx=15,
            pady=8,
            command=self.borrow_book
        ).grid(row=2, column=1, sticky="w", pady=25, padx=(15, 0))

        # Info label
        self.borrow_info = tk.Label(
            form_frame,
            text="",
            font=self.small_font,
            bg="white",
            fg="#27ae60"
        )
        self.borrow_info.grid(row=3, column=0, columnspan=2, pady=10)

        # Bind Enter key
        self.borrow_user_entry.bind("<Return>", lambda e: self.borrow_book_entry.focus())
        self.borrow_book_entry.bind("<Return>", lambda e: self.borrow_book())

    def build_return_tab(self, parent):
        """Build return tab với tính phạt tự động"""
        # Main container với padding
        main_frame = tk.Frame(parent, bg="white")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas và scrollbar để cuộn nếu nội dung dài
        canvas = tk.Canvas(main_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form container
        form_frame = tk.Frame(scrollable_frame, bg="white", padx=25, pady=20)
        form_frame.pack()
        
        # ===== PHẦN 1: THÔNG TIN ĐƠN MƯỢN =====
        info_frame = tk.LabelFrame(form_frame, text=" THÔNG TIN ĐƠN MƯỢN ", 
                                  font=("Arial", 11, "bold"), 
                                  bg="white", fg="#2c3e50",
                                  padx=15, pady=12,
                                  relief="solid", bd=1)
        info_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15), padx=5)
        info_frame.grid_columnconfigure(1, weight=1)

        # Mã đơn mượn
        tk.Label(
            info_frame, 
            text="Mã đơn mượn (Borrow ID):", 
            font=self.label_font,
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))
        
        self.return_borrow_entry = tk.Entry(
            info_frame, 
            width=40,
            font=self.entry_font,
            relief="solid",
            bd=1
        )
        self.return_borrow_entry.grid(row=0, column=1, pady=8, sticky="ew")

        # ===== PHẦN 2: NGÀY THỰC TẾ =====
        date_frame = tk.LabelFrame(form_frame, text=" NGÀY THỰC TẾ (TÙY CHỌN) ", 
                                  font=("Arial", 11, "bold"), 
                                  bg="white", fg="#2c3e50",
                                  padx=15, pady=12,
                                  relief="solid", bd=1)
        date_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15), padx=5)
        date_frame.grid_columnconfigure(1, weight=1)

        # Ngày mượn thực tế
        date_row1 = tk.Frame(date_frame, bg="white")
        date_row1.grid(row=0, column=0, columnspan=2, sticky="ew", pady=6)
        
        tk.Label(
            date_row1, 
            text="Ngày mượn thực tế:", 
            font=self.label_font,
            bg="white",
            width=20,
            anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        self.actual_borrow_date_entry = tk.Entry(
            date_row1, 
            width=25,
            font=self.entry_font,
            relief="solid",
            bd=1
        )
        self.actual_borrow_date_entry.pack(side="left")
        self.actual_borrow_date_entry.insert(0, "")
        
        # Ghi chú định dạng ngày mượn
        format_label1 = tk.Label(
            date_row1,
            text="(Định dạng: YYYY-MM-DD)",
            font=("Arial", 9, "italic"),
            bg="white",
            fg="#7f8c8d"
        )
        format_label1.pack(side="left", padx=(10, 0))

        # Ngày trả thực tế
        date_row2 = tk.Frame(date_frame, bg="white")
        date_row2.grid(row=1, column=0, columnspan=2, sticky="ew", pady=6)
        
        tk.Label(
            date_row2, 
            text="Ngày trả thực tế:", 
            font=self.label_font,
            bg="white",
            width=20,
            anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        self.actual_return_date_entry = tk.Entry(
            date_row2, 
            width=25,
            font=self.entry_font,
            relief="solid",
            bd=1
        )
        self.actual_return_date_entry.pack(side="left")
        self.actual_return_date_entry.insert(0, "")
        
        # Ghi chú định dạng ngày trả
        format_label2 = tk.Label(
            date_row2,
            text="(Định dạng: YYYY-MM-DD)",
            font=("Arial", 9, "italic"),
            bg="white",
            fg="#7f8c8d"
        )
        format_label2.pack(side="left", padx=(10, 0))

        # ===== PHẦN 3: TÌNH TRẠNG SÁCH =====
        condition_frame = tk.LabelFrame(form_frame, text=" TÌNH TRẠNG SÁCH KHI TRẢ ", 
                                       font=("Arial", 11, "bold"), 
                                       bg="white", fg="#2c3e50",
                                       padx=15, pady=12,
                                       relief="solid", bd=1)
        condition_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 15), padx=5)

        tk.Label(
            condition_frame, 
            text="Chọn tình trạng sách:", 
            font=self.label_font,
            bg="white"
        ).pack(side="left", padx=(0, 15))
        
        self.condition_var = tk.StringVar(value="GOOD")
        condition_menu = tk.OptionMenu(
            condition_frame, 
            self.condition_var, 
            "GOOD", "DAMAGED", "TORN", "LOST"
        )
        condition_menu.config(
            width=15,
            font=self.entry_font,
            bg="#f8f9fa",
            relief="solid",
            bd=1
        )
        condition_menu.pack(side="left")

        # ===== PHẦN 4: QUY ĐỊNH PHẠT =====
        fine_frame = tk.LabelFrame(form_frame, text=" ⚠️ QUY ĐỊNH PHẠT ", 
                                  font=("Arial", 11, "bold"), 
                                  bg="#f8f9fa", fg="#2c3e50",
                                  padx=15, pady=12,
                                  relief="solid", bd=1)
        fine_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 20), padx=5)

        # Tạo frame cho nội dung quy định phạt
        fine_content = tk.Frame(fine_frame, bg="#f8f9fa")
        fine_content.pack(fill="x", padx=5)

        # Danh sách quy định phạt với định dạng đẹp
        fine_rules = [
            "• GOOD: Không phạt",
            "• DAMAGED: Phạt 50,000 VND",
            "• TORN: Phạt 100,000 VND",
            "• LOST: Phạt 200,000 VND",
            "• Trả trễ: 5,000 VND/ngày",
            "• Hệ thống tự tính phạt dựa trên tình trạng sách và ngày thực tế"
        ]
        
        for rule in fine_rules:
            tk.Label(
                fine_content,
                text=rule,
                font=self.small_font,
                bg="#f8f9fa",
                fg="#2c3e50",
                justify="left",
                anchor="w"
            ).pack(fill="x", pady=2)

        # ===== PHẦN 5: NÚT TRẢ SÁCH & XÓA DỮ LIỆU =====
        button_frame = tk.Frame(form_frame, bg="white", pady=15)
        button_frame.grid(row=4, column=0, columnspan=2, sticky="ew")

        # Frame cho các nút
        buttons_row = tk.Frame(button_frame, bg="white")
        buttons_row.pack()

        # Nút TRẢ SÁCH (tự động tính phạt)
        return_button = tk.Button(
            buttons_row,
            text="TRẢ SÁCH",
            width=20,
            height=2,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            relief="raised",
            bd=2,
            padx=15,
            pady=8,
            command=self.return_book_with_fine
        )
        return_button.pack(side="left", padx=(0, 15))

        # Nút XÓA DỮ LIỆU NHẬP
        clear_button = tk.Button(
            buttons_row,
            text="🗑 XÓA DỮ LIỆU",
            width=15,
            height=2,
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            relief="raised",
            bd=2,
            padx=10,
            pady=8,
            command=self.clear_return_form
        )
        clear_button.pack(side="left")

        # Thêm hiệu ứng hover cho nút
        def on_enter_return(e):
            return_button['background'] = '#2980b9'
            
        def on_leave_return(e):
            return_button['background'] = '#3498db'
            
        def on_enter_clear(e):
            clear_button['background'] = '#c0392b'
            
        def on_leave_clear(e):
            clear_button['background'] = '#e74c3c'
            
        return_button.bind("<Enter>", on_enter_return)
        return_button.bind("<Leave>", on_leave_return)
        clear_button.bind("<Enter>", on_enter_clear)
        clear_button.bind("<Leave>", on_leave_clear)

        # Info label
        self.return_info = tk.Label(
            form_frame,
            text="",
            font=("Arial", 10),
            bg="white",
            fg="#27ae60"
        )
        self.return_info.grid(row=5, column=0, columnspan=2, pady=10)

        # Bind Enter key
        self.return_borrow_entry.bind("<Return>", lambda e: self.return_book_with_fine())

        # Configure grid weights
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Pack canvas và scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Chỉ hiện scrollbar khi cần
        def check_scrollbar():
            canvas.update_idletasks()
            if canvas.bbox("all")[3] > canvas.winfo_height():
                scrollbar.pack(side="right", fill="y")
            else:
                scrollbar.pack_forget()
        
        canvas.bind("<Configure>", lambda e: check_scrollbar())

    def build_history_tab(self, parent):
        """Build history tab với nút xóa dữ liệu"""
        # Main container
        main_frame = tk.Frame(parent, bg="white")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # User ID input frame
        input_frame = tk.Frame(main_frame, bg="white", padx=20, pady=12)
        input_frame.pack(fill="x")

        tk.Label(
            input_frame, 
            text="User ID:", 
            font=self.label_font,
            bg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.history_user_entry = tk.Entry(
            input_frame, 
            width=20,
            font=self.entry_font,
            relief="solid",
            bd=1
        )
        self.history_user_entry.pack(side="left", padx=(0, 15))
        
        # Frame cho các nút tìm kiếm
        search_buttons_frame = tk.Frame(input_frame, bg="white")
        search_buttons_frame.pack(side="left", padx=(0, 15))
        
        tk.Button(
            search_buttons_frame,
            text="🔍 Xem lịch sử",
            font=self.entry_font,
            bg="#3498db",
            fg="white",
            relief="raised",
            bd=1,
            padx=15,
            pady=5,
            command=self.load_borrow_history
        ).pack(side="left", padx=(0, 10))

        # Nút xóa dữ liệu trong history tab
        tk.Button(
            search_buttons_frame,
            text="🗑 XÓA DỮ LIỆU",
            font=self.entry_font,
            bg="#e74c3c",
            fg="white",
            relief="raised",
            bd=1,
            padx=15,
            pady=5,
            command=self.clear_history_form
        ).pack(side="left")

        # Table frame
        table_frame = tk.Frame(main_frame, bg="white", padx=20)
        table_frame.pack(pady=10, fill="both", expand=True)

        # Create Treeview với style đẹp hơn
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                       font=self.entry_font,
                       rowheight=25)
        style.configure("Custom.Treeview.Heading", 
                       font=("Arial", 10, "bold"),
                       background="#ecf0f1")

        columns = ("Mã mượn", "User ID", "Ngày mượn", "Hạn trả", "Ngày trả", "Trạng thái", "Phạt")
        self.history_tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings",
            height=12,
            style="Custom.Treeview"
        )

        # Define headings
        column_widths = [120, 80, 110, 110, 110, 100, 100]
        for col, width in zip(columns, column_widths):
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=width, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.history_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)

        # Bind Enter key
        self.history_user_entry.bind("<Return>", lambda e: self.load_borrow_history())

    def clear_return_form(self):
        """Xóa tất cả dữ liệu nhập trong tab Trả sách"""
        self.return_borrow_entry.delete(0, tk.END)
        self.actual_borrow_date_entry.delete(0, tk.END)
        self.actual_return_date_entry.delete(0, tk.END)
        self.condition_var.set("GOOD")
        self.return_info.config(text="Đã xóa dữ liệu nhập", fg="#27ae60")
        
    def clear_history_form(self):
        """Xóa tất cả dữ liệu trong tab Lịch sử"""
        self.history_user_entry.delete(0, tk.END)
        # Clear tree
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        # Hiển thị thông báo trống
        self.history_tree.insert("", "end", values=("Dữ liệu đã được xóa", "", "", "", "", "", ""))

    # ===== CÁC HÀM XỬ LÝ CHỨC NĂNG (GIỮ NGUYÊN) =====
    
    def borrow_book(self):
        """Handle borrow book action"""
        user_id = self.borrow_user_entry.get().strip()
        book_id = self.borrow_book_entry.get().strip()

        if not user_id or not book_id:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập User ID và Book ID.")
            return

        if not user_id.isdigit():
            messagebox.showwarning("Sai định dạng", "User ID phải là số.")
            return

        try:
            result = self.borrow_service.borrow_book(int(user_id), book_id)
            if result.get("success"):
                messagebox.showinfo("Thành công", result.get("message", "Mượn sách thành công"))
                self.borrow_info.config(text=result.get("message"), fg="#27ae60")
                self.borrow_user_entry.delete(0, tk.END)
                self.borrow_book_entry.delete(0, tk.END)
                self.borrow_user_entry.focus()
            else:
                messagebox.showerror("Lỗi", result.get("message", "Không thể mượn sách"))
                self.borrow_info.config(text=result.get("message"), fg="#e74c3c")
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Lỗi: {str(e)}")
            self.borrow_info.config(text=f"Lỗi: {str(e)}", fg="#e74c3c")

    def return_book(self):
        """Handle return book action (không tính phạt)"""
        borrow_id = self.return_borrow_entry.get().strip()

        if not borrow_id:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã đơn mượn.")
            return

        try:
            result = self.borrow_service.return_book(borrow_id)
            if result.get("success"):
                messagebox.showinfo("Thành công", result.get("message", "Trả sách thành công"))
                self.return_info.config(text=result.get("message"), fg="#27ae60")
                self.return_borrow_entry.delete(0, tk.END)
                self.return_borrow_entry.focus()
            else:
                messagebox.showerror("Lỗi", result.get("message", "Không thể trả sách"))
                self.return_info.config(text=result.get("message"), fg="#e74c3c")
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Lỗi: {str(e)}")
            self.return_info.config(text=f"Lỗi: {str(e)}", fg="#e74c3c")

    def return_book_with_fine(self):
        """Trả sách có tính phạt tự động"""
        borrow_id = self.return_borrow_entry.get().strip()
        condition = self.condition_var.get()
        actual_borrow_date = self.actual_borrow_date_entry.get().strip()
        actual_return_date = self.actual_return_date_entry.get().strip()
        
        if not borrow_id:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã đơn mượn.")
            return
        
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
                
                # Clear input
                self.return_borrow_entry.delete(0, tk.END)
                self.actual_borrow_date_entry.delete(0, tk.END)
                self.actual_return_date_entry.delete(0, tk.END)
                self.return_info.config(text="Trả sách thành công", fg="#27ae60")
                
                # Refresh history tab nếu đang xem
                if self.history_user_entry.get():
                    self.load_borrow_history()
            else:
                messagebox.showerror("Lỗi", result.get("message", "Không thể trả sách"))
                self.return_info.config(text=result.get("message"), fg="#e74c3c")
                
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Lỗi: {str(e)}")
            self.return_info.config(text=f"Lỗi: {str(e)}", fg="#e74c3c")

    def load_borrow_history(self):
        """Load borrow history for user"""
        user_id = self.history_user_entry.get().strip()

        if not user_id:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập User ID.")
            return

        if not user_id.isdigit():
            messagebox.showwarning("Sai định dạng", "User ID phải là số.")
            return

        try:
            # Clear existing items
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)

            # Get user borrows
            borrows = self.borrow_service.get_user_borrows(int(user_id))
            
            if not borrows:
                self.history_tree.insert("", "end", values=("Không có dữ liệu", "", "", "", "", "", ""))
                return

            # Insert borrows into table
            for borrow in borrows:
                status_text = {
                    "BORROWED": "Đang mượn",
                    "RETURNED": "Đã trả",
                    "OVERDUE": "Quá hạn",
                    "PENDING": "Đang chờ"
                }.get(borrow.get("status", ""), borrow.get("status", ""))

                # Hiển thị phạt nếu có
                fine_amount = borrow.get("fine_amount", 0)
                fine_text = f"{fine_amount:,} VND" if fine_amount > 0 else "Không"
                
                # Lấy ngày thực tế nếu có
                borrow_date = borrow.get("actual_borrow_date", borrow.get("borrow_date", ""))
                return_date = borrow.get("actual_return_date", borrow.get("return_date", ""))

                self.history_tree.insert("", "end", values=(
                    borrow.get("borrow_id", ""),
                    borrow.get("user_id", ""),
                    borrow_date[:10] if borrow_date else "",
                    borrow.get("due_date", "")[:10] if borrow.get("due_date") else "",
                    return_date[:10] if return_date else "",
                    status_text,
                    fine_text
                ))
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Lỗi khi tải lịch sử: {str(e)}")