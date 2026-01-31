# services/fine_service.py
from utils.file_handler_fix import load_json, save_json
from config import FINE_PER_DAY  # ĐÃ SỬA: THÊM IMPORT NÀY
from datetime import datetime
import uuid


class FineService:
    def __init__(self, fine_path="data/fines.json", borrow_path="data/borrow_orders.json"):
        self.fine_path = fine_path
        self.borrow_path = borrow_path

    def calculate_fine(self, overdue_days: int) -> int:
        """Tính tiền phạt dựa trên số ngày quá hạn"""
        if overdue_days <= 0:
            return 0
        return overdue_days * FINE_PER_DAY  # ĐÃ SỬA: DÙNG BIẾN TỪ CONFIG

    def add_fine(self, user_id: int, borrow_id: str, amount: int, reason: str = "") -> bool:
        """Thêm tiền phạt cho user"""
        try:
            fines = load_json(self.fine_path)
            
            # KIỂM TRA TRÙNG: Không thêm phạt nếu đã có phạt chưa thanh toán cho đơn này
            existing_fine = next(
                (f for f in fines if f.get("borrow_id") == borrow_id and f.get("status") == "UNPAID"),
                None
            )
            
            if existing_fine:
                print(f"⚠️ Đã có phạt chưa thanh toán cho đơn mượn {borrow_id}")
                return False
            
            fines.append({
                "fine_id": str(uuid.uuid4()),
                "user_id": user_id,
                "borrow_id": borrow_id,
                "amount": amount,
                "reason": reason,
                "status": "UNPAID",
                "created_date": datetime.now().isoformat(),
                "paid_date": None
            })

            save_json(self.fine_path, fines)
            return True
        except Exception as e:
            print(f"❌ Error adding fine: {e}")
            return False

    def get_user_fines(self, user_id: int):
        """Lấy danh sách tiền phạt của user"""
        try:
            fines = load_json(self.fine_path)
            user_fines = [f for f in fines if f.get("user_id") == user_id]
            return user_fines
        except Exception as e:
            print(f"❌ Error getting user fines: {e}")
            return []

    def get_unpaid_fines(self, user_id: int):
        """Lấy danh sách tiền phạt chưa thanh toán của user"""
        try:
            fines = load_json(self.fine_path)
            unpaid_fines = [
                f for f in fines 
                if f.get("user_id") == user_id and f.get("status") == "UNPAID"
            ]
            return unpaid_fines
        except Exception as e:
            print(f"❌ Error getting unpaid fines: {e}")
            return []

    def pay_fine(self, fine_id: str) -> dict:
        """Thanh toán tiền phạt"""
        try:
            fines = load_json(self.fine_path)
            
            for fine in fines:
                if fine.get("fine_id") == fine_id:
                    if fine.get("status") == "PAID":
                        return {"success": False, "message": "💰 Tiền phạt đã được thanh toán trước đó"}
                    
                    fine["status"] = "PAID"
                    fine["paid_date"] = datetime.now().isoformat()
                    
                    save_json(self.fine_path, fines)
                    return {
                        "success": True, 
                        "message": "✅ Thanh toán thành công",
                        "amount": fine.get("amount", 0)
                    }
            
            return {"success": False, "message": "❌ Không tìm thấy tiền phạt"}
        except Exception as e:
            print(f"❌ Error paying fine: {e}")
            return {"success": False, "message": f"Lỗi hệ thống: {str(e)}"}

    def calculate_overdue_fines(self) -> int:
        """
        Tính và cập nhật tiền phạt cho các đơn mượn quá hạn CHƯA CÓ PHẠT
        Trả về: số phạt đã thêm
        """
        try:
            borrows = load_json(self.borrow_path)
            fines = load_json(self.fine_path)
            now = datetime.now()
            
            fines_added = 0
            
            for borrow in borrows:
                if borrow.get("status") == "BORROWED":
                    due_date_str = borrow.get("due_date")
                    if due_date_str:
                        try:
                            due_date = datetime.fromisoformat(due_date_str)
                            if due_date < now:
                                overdue_days = (now - due_date).days
                                if overdue_days > 0:
                                    # Kiểm tra xem đã có phạt cho đơn này chưa
                                    borrow_id = borrow.get("borrow_id")
                                    existing_fine = next(
                                        (f for f in fines if f.get("borrow_id") == borrow_id),
                                        None
                                    )
                                    
                                    if not existing_fine:  # Chỉ tạo nếu chưa có phạt
                                        amount = self.calculate_fine(overdue_days)
                                        if amount > 0:
                                            success = self.add_fine(
                                                user_id=borrow.get("user_id"),
                                                borrow_id=borrow_id,
                                                amount=amount,
                                                reason=f"Trả trễ {overdue_days} ngày"
                                            )
                                            if success:
                                                fines_added += 1
                        except Exception as e:
                            print(f"⚠️ Error processing borrow {borrow.get('borrow_id')}: {e}")
                            continue
            
            return fines_added
        except Exception as e:
            print(f"❌ Error calculating overdue fines: {e}")
            return 0

    def get_total_unpaid_amount(self, user_id: int) -> int:
        """Tính tổng tiền phạt chưa thanh toán của user"""
        try:
            unpaid_fines = self.get_unpaid_fines(user_id)
            total = sum(fine.get("amount", 0) for fine in unpaid_fines)
            return total
        except Exception as e:
            print(f"❌ Error calculating total unpaid amount: {e}")
            return 0

    def get_fine_by_borrow_id(self, borrow_id: str):
        """Lấy thông tin phạt theo borrow_id"""
        try:
            fines = load_json(self.fine_path)
            fine = next((f for f in fines if f.get("borrow_id") == borrow_id), None)
            return fine
        except Exception as e:
            print(f"❌ Error getting fine by borrow_id: {e}")
            return None

    def update_fine_amount(self, fine_id: str, new_amount: int, reason: str = "") -> bool:
        """Cập nhật số tiền phạt (admin)"""
        try:
            fines = load_json(self.fine_path)
            
            for fine in fines:
                if fine.get("fine_id") == fine_id:
                    fine["amount"] = new_amount
                    if reason:
                        fine["reason"] = reason
                    save_json(self.fine_path, fines)
                    return True
            
            return False
        except Exception as e:
            print(f"❌ Error updating fine amount: {e}")
            return False

    def get_all_fines(self):
        """Lấy tất cả tiền phạt (admin)"""
        try:
            fines = load_json(self.fine_path)
            return fines
        except Exception as e:
            print(f"❌ Error getting all fines: {e}")
            return []

    def delete_fine(self, fine_id: str) -> bool:
        """Xóa phạt (admin)"""
        try:
            fines = load_json(self.fine_path)
            
            new_fines = [f for f in fines if f.get("fine_id") != fine_id]
            
            if len(new_fines) < len(fines):  # Có xóa
                save_json(self.fine_path, new_fines)
                return True
            return False
        except Exception as e:
            print(f"❌ Error deleting fine: {e}")
            return False