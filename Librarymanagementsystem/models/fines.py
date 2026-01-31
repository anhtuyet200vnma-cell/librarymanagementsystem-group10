import sys
import os
import uuid
from datetime import datetime

# Thêm đường dẫn project để import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import FINE_PER_DAY  # ĐÃ SỬA: IMPORT TỪ CONFIG
except ImportError:
    # Fallback nếu không tìm thấy config
    FINE_PER_DAY = 5000
    print("⚠️  Warning: Không tìm thấy config.FINE_PER_DAY, sử dụng giá trị mặc định 5000")

def generate_id():
    return uuid.uuid4().hex[:8] 

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Fine:
    """Fine class - Phạt"""
    
    def __init__(self, fine_id=None, borrow_order_detail_id=None,
                 amount=0.0, reason=None, paid_status=False,
                 created_date=None, user_id=None, borrow_id=None):  # THÊM THAM SỐ MỚI
        self.fine_id = fine_id or generate_id()
        self.borrow_order_detail_id = borrow_order_detail_id
        self.user_id = user_id  # THÊM
        self.borrow_id = borrow_id  # THÊM
        self.amount = float(amount)
        self.reason = reason
        self.paid_status = bool(paid_status)
        self.created_date = created_date or get_current_datetime()
    
    def calculate_fines(self, overdue_days: int, condition: str = None):
        amount = 0.0
        reasons = []
        
        if overdue_days > 0:
            overdue_fine = overdue_days * FINE_PER_DAY  # ĐÃ SỬA: DÙNG BIẾN TỪ CONFIG
            amount += overdue_fine
            reasons.append(f"Trả trễ {overdue_days} ngày: {overdue_fine:,.0f} VND")
        
        if condition == 'DAMAGED':
            damage_fine = 50000
            amount += damage_fine
            reasons.append(f"Sách bị hư hỏng: {damage_fine:,.0f} VND")
        elif condition == 'TORN':
            torn_fine = 100000 
            amount += torn_fine
            reasons.append(f"Sách bị rách: {torn_fine:,.0f} VND")
        elif condition == 'LOST':
            lost_fine = 500000
            amount += lost_fine
            reasons.append(f"Mất sách: {lost_fine:,.0f} VND")
        
        self.amount = amount
        self.reason = "; ".join(reasons) if reasons else "Không có tiền phạt"
        return self.amount
    
    @classmethod
    def create_fine(cls, detail_obj, overdue_days: int):
        condition = None
        borrow_order_detail_id = None
        
        if hasattr(detail_obj, 'condition'):
            condition = detail_obj.condition
        if hasattr(detail_obj, 'borrow_order_detail_id'):
            borrow_order_detail_id = detail_obj.borrow_order_detail_id
            
        new_fine = cls(borrow_order_detail_id=borrow_order_detail_id)
        new_fine.calculate_fines(overdue_days, condition)
        
        if new_fine.amount <= 0:
            return None, "Không có tiền phạt"
            
        return new_fine, None
    
    def pay_fine(self):
        if self.paid_status:
            return False, "Phạt đã được thanh toán"
        
        self.paid_status = True
        return True, None
    
    def get_amount_formatted(self):
        return f"{self.amount:,.0f} VND"
    
    def to_dict(self):
        return {
            'fine_id': self.fine_id,
            'borrow_order_detail_id': self.borrow_order_detail_id,
            'user_id': self.user_id,  # THÊM
            'borrow_id': self.borrow_id,  # THÊM
            'amount': self.amount,
            'reason': self.reason,
            'paid_status': self.paid_status,
            'created_date': self.created_date
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            fine_id=data.get('fine_id'),
            borrow_order_detail_id=data.get('borrow_order_detail_id'),
            user_id=data.get('user_id'),  # THÊM
            borrow_id=data.get('borrow_id'),  # THÊM
            amount=float(data.get('amount', 0.0)),
            reason=data.get('reason'),
            paid_status=bool(data.get('paid_status', False)),
            created_date=data.get('created_date')
        )
    
    def __str__(self):
        status = "✅ Đã thanh toán" if self.paid_status else "❌ Chưa thanh toán"
        return f"Fine({self.get_amount_formatted()} - {status})"
    
    def __repr__(self):
        return f"Fine(id={self.fine_id}, amount={self.amount}, paid={self.paid_status})"