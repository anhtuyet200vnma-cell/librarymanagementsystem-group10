ORDER_STATUS = {
    'BORROWED': 'BORROWED',
    'RETURNED': 'RETURNED',
    'LOST': 'LOST',
    'DAMAGED': 'DAMAGED'
}


class BorrowOrderDetail:
    """Chi tiết từng cuốn sách trong đơn mượn"""
    
    def __init__(self, book_id, item_status=ORDER_STATUS['BORROWED'],
                 condition=None, actual_return_date=None):
        self.book_id = book_id
        self.item_status = item_status
        self.condition = condition
        self.actual_return_date = actual_return_date
    
    def mark_as_returned(self, return_date, condition):
        """
        Mark item as returned
        Returns: (success, error_message)
        """
        self.item_status = ORDER_STATUS['RETURNED']
        self.actual_return_date = return_date
        self.condition = condition
        return True, None
    
    def is_returned(self):
        """Check if item is returned"""
        return self.item_status == ORDER_STATUS['RETURNED']
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'book_id': self.book_id,
            'item_status': self.item_status,
            'condition': self.condition,
            'actual_return_date': self.actual_return_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        return cls(**data)
    
    def __str__(self):
        return f"OrderDetail(book={self.book_id}, status={self.item_status})"
    
    def __repr__(self):
        return f"BorrowOrderDetail(book_id='{self.book_id}', status='{self.item_status}')"