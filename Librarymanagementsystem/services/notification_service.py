# services/notification_service.py
from utils.file_handler_fix import load_json, save_json
from datetime import datetime
import uuid


class NotificationService:
    def __init__(self, path="data/notifications.json"):
        self.path = path

    def send_notification(self, user_id: int, content: str, notification_type: str = "SYSTEM") -> bool:
        """Gửi thông báo cho user"""
        try:
            notifications = load_json(self.path)

            notifications.append({
                "notification_id": str(uuid.uuid4()),
                "user_id": user_id,
                "content": content,
                "type": notification_type,
                "created_date": datetime.now().isoformat(),
                "status": "SENT",
                "is_read": False
            })

            save_json(self.path, notifications)
            return True
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False

    def get_user_notifications(self, user_id: int, unread_only: bool = False):
        """Lấy thông báo của user"""
        try:
            notifications = load_json(self.path)
            
            user_notifications = [
                n for n in notifications 
                if n.get("user_id") == user_id
            ]
            
            if unread_only:
                user_notifications = [
                    n for n in user_notifications 
                    if not n.get("is_read", False)
                ]
            
            # Sắp xếp theo thời gian mới nhất
            user_notifications.sort(
                key=lambda x: x.get("created_date", ""), 
                reverse=True
            )
            
            return user_notifications
        except Exception as e:
            print(f"Error getting user notifications: {e}")
            return []

    def mark_as_read(self, notification_id: str) -> bool:
        """Đánh dấu thông báo đã đọc"""
        try:
            notifications = load_json(self.path)
            
            for notification in notifications:
                if notification.get("notification_id") == notification_id:
                    notification["is_read"] = True
                    save_json(self.path, notifications)
                    return True
            
            return False
        except Exception as e:
            print(f"Error marking notification as read: {e}")
            return False

    def mark_all_as_read(self, user_id: int) -> bool:
        """Đánh dấu tất cả thông báo của user là đã đọc"""
        try:
            notifications = load_json(self.path)
            
            updated = False
            for notification in notifications:
                if notification.get("user_id") == user_id:
                    notification["is_read"] = True
                    updated = True
            
            if updated:
                save_json(self.path, notifications)
            
            return updated
        except Exception as e:
            print(f"Error marking all notifications as read: {e}")
            return False

    def send_overdue_notification(self, user_id: int, borrow_id: str, overdue_days: int):
        """Gửi thông báo quá hạn"""
        content = f"Bạn có đơn mượn #{borrow_id[:8]} quá hạn {overdue_days} ngày. Vui lòng trả sách."
        return self.send_notification(
            user_id=user_id,
            content=content,
            notification_type="OVERDUE"
        )

    def send_borrow_confirmation(self, user_id: int, borrow_id: str):
        """Gửi thông báo xác nhận mượn sách"""
        content = f"Đơn mượn #{borrow_id[:8]} đã được xử lý thành công."
        return self.send_notification(
            user_id=user_id,
            content=content,
            notification_type="BORROW_CONFIRMATION"
        )

    def send_return_confirmation(self, user_id: int, borrow_id: str):
        """Gửi thông báo xác nhận trả sách"""
        content = f"Đơn mượn #{borrow_id[:8]} đã được trả thành công."
        return self.send_notification(
            user_id=user_id,
            content=content,
            notification_type="RETURN_CONFIRMATION"
        )

    def delete_notification(self, notification_id: str) -> bool:
        """Xóa thông báo"""
        try:
            notifications = load_json(self.path)
            
            new_notifications = [
                n for n in notifications 
                if n.get("notification_id") != notification_id
            ]
            
            if len(new_notifications) < len(notifications):
                save_json(self.path, new_notifications)
                return True
            
            return False
        except Exception as e:
            print(f"Error deleting notification: {e}")
            return False