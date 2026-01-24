# models/__init__.py
# Import tất cả class theo đặc tả

# User và các lớp con
from .user import User
from .admin import Admin
from .member import Member

# Book và liên quan
from .book import Book
from .author import Author
from .category import Category

# Borrowing system
from .borrow_request import BorrowRequest
from .borrow_order import BorrowOrder
from .borrow_order_detail import BorrowOrderDetail

# Supporting classes
from .fine import Fine
from .notification import Notification
from .waiting_list import WaitingList
from .waiting_list_item import WaitingListItem
from .role import Role

# Service layer (theo đặc tả trang 60-61)
from .book_service import BookService

__all__ = [
    'User',
    'Admin', 
    'Member',
    'Book',
    'Author',
    'Category',
    'BorrowRequest',
    'BorrowOrder',
    'BorrowOrderDetail',
    'Fine',
    'Notification',
    'WaitingList',
    'WaitingListItem',
    'Role',
    'BookService'
]