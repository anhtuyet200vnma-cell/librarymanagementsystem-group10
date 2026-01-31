import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookUI(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # File paths
        self.data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data"
        )
        self.books_file = os.path.join(self.data_dir, "books.json")
        self.authors_file = os.path.join(self.data_dir, "authors.json")
        self.categories_file = os.path.join(self.data_dir, "categories.json")

        self.build_ui()
        self.load_books()

    def load_books_data(self):
        """Load books data from JSON files"""
        books = []
        try:
            # Load books
            if os.path.exists(self.books_file):
                with open(self.books_file, "r", encoding="utf-8") as f:
                    books_data = json.load(f)
            else:
                books_data = []
            
            # Load authors for mapping
            authors_map = {}
            if os.path.exists(self.authors_file):
                with open(self.authors_file, "r", encoding="utf-8") as f:
                    authors_data = json.load(f)
                    for author in authors_data:
                        authors_map[author.get("author_id")] = author.get("author_name", "Unknown")
            
            # Load categories for mapping
            categories_map = {}
            if os.path.exists(self.categories_file):
                with open(self.categories_file, "r", encoding="utf-8") as f:
                    categories_data = json.load(f)
                    for category in categories_data:
                        categories_map[category.get("category_id")] = category.get("category_name", "Unknown")
            
            # Transform data
            for book in books_data:
                author_name = authors_map.get(book.get("author_id"), "Unknown")
                category_name = categories_map.get(book.get("category_id"), "Unknown")
                
                books.append({
                    "book_id": book.get("book_id", ""),
                    "title": book.get("title", ""),
                    "author": author_name,
                    "category": category_name,
                    "year": book.get("publication_year", ""),
                    "quantity": book.get("quantity", 0),
                    "available": book.get("available_quantity", 0),
                    "status": book.get("status", "UNKNOWN")
                })
            
        except Exception as e:
            print(f"Error loading books data: {e}")
        
        return books

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
            text="QUẢN LÝ SÁCH", 
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=10)

        # Search frame
        search_frame = tk.Frame(self, bg="white")
        search_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(
            search_frame, 
            text="Tìm kiếm:", 
            font=("Arial", 11),
            bg="white"
        ).pack(side="left", padx=(0, 10))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame, 
            textvariable=self.search_var,
            width=40,
            font=("Arial", 11),
            relief="solid"
        )
        search_entry.pack(side="left", padx=(0, 10))
        
        tk.Button(
            search_frame,
            text="🔍 Tìm",
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            command=self.search_books
        ).pack(side="left")

        tk.Button(
            search_frame,
            text="🔄 Làm mới",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            command=self.load_books
        ).pack(side="left", padx=(10, 0))

        # Table frame
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Create Treeview
        columns = ("ID", "Title", "Author", "Category", "Year", "Total", "Available", "Status")
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings",
            height=15,
            style="Treeview"
        )

        # Define headings
        column_widths = [80, 250, 150, 120, 80, 70, 80, 100]
        for col, width in zip(columns, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center" if col in ["ID", "Year", "Total", "Available"] else "w")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)

        # Status colors
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        # Info label
        self.info_label = tk.Label(
            self,
            text="",
            font=("Arial", 10),
            bg="white",
            fg="#27ae60"
        )
        self.info_label.pack(pady=10)

        # Bind search on Enter
        search_entry.bind("<Return>", lambda e: self.search_books())

    def load_books(self):
        """Load all books into the table"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load books data
        books = self.load_books_data()
        
        # Insert books into table
        for book in books:
            status = book["status"]
            status_text = {
                "AVAILABLE": "Có sẵn",
                "UNAVAILABLE": "Đã hết",
                "RESERVED": "Đặt trước",
                "LOST": "Đã mất",
                "DAMAGED": "Hư hỏng"
            }.get(status, status)
            
            # Color coding for status
            tags = ()
            if status == "AVAILABLE":
                tags = ("available",)
            elif status == "UNAVAILABLE":
                tags = ("unavailable",)
            
            self.tree.insert("", "end", values=(
                book["book_id"],
                book["title"],
                book["author"],
                book["category"],
                book["year"],
                book["quantity"],
                book["available"],
                status_text
            ), tags=tags)
        
        # Configure tag colors
        self.tree.tag_configure("available", background="#d5f4e6")
        self.tree.tag_configure("unavailable", background="#f4d5d5")
        
        self.info_label.config(text=f"Đã tải {len(books)} cuốn sách")

    def search_books(self):
        """Search books based on keyword"""
        keyword = self.search_var.get().strip().lower()
        
        if not keyword:
            self.load_books()
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load and filter books
        books = self.load_books_data()
        filtered_books = [
            book for book in books 
            if (keyword in book["title"].lower() or 
                keyword in book["author"].lower() or 
                keyword in book["book_id"].lower() or
                keyword in book["category"].lower())
        ]
        
        # Insert filtered books
        for book in filtered_books:
            status_text = {
                "AVAILABLE": "Có sẵn",
                "UNAVAILABLE": "Đã hết",
                "RESERVED": "Đặt trước",
                "LOST": "Đã mất",
                "DAMAGED": "Hư hỏng"
            }.get(book["status"], book["status"])
            
            tags = ()
            if book["status"] == "AVAILABLE":
                tags = ("available",)
            elif book["status"] == "UNAVAILABLE":
                tags = ("unavailable",)
            
            self.tree.insert("", "end", values=(
                book["book_id"],
                book["title"],
                book["author"],
                book["category"],
                book["year"],
                book["quantity"],
                book["available"],
                status_text
            ), tags=tags)
        
        self.info_label.config(text=f"Tìm thấy {len(filtered_books)} kết quả cho '{keyword}'")