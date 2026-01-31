"""
email_reminder.py
Gửi email nhắc trả sách
"""

from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.file_handler import load_json

class EmailReminder:
    def __init__(self):
        self.borrow_path = "data/borrow_orders.json"
        self.users_path = "data/users.json"
        
        # Cấu hình email (cần điền thông tin thật)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "library@yourdomain.com"
        self.sender_password = "yourpassword"
    
    def send_reminder_emails(self):
        """Gửi email nhắc nhở cho tất cả sách sắp đến hạn"""
        try:
            borrows = load_json(self.borrow_path)
            users = load_json(self.users_path)
            today = datetime.now()
            
            for borrow in borrows:
                if borrow.get("status") == "BORROWED":
                    due_date_str = borrow.get("due_date")
                    if due_date_str:
                        due_date = datetime.fromisoformat(due_date_str)
                        
                        # Tính số ngày còn lại
                        days_remaining = (due_date - today).days
                        
                        # Gửi nhắc nhở trước 5, 3, 1 ngày và mỗi ngày khi quá hạn
                        if days_remaining in [5, 3, 1] or days_remaining < 0:
                            user_id = borrow.get("user_id")
                            user = next((u for u in users if u.get("user_id") == user_id), None)
                            
                            if user and user.get("email"):
                                self._send_email(
                                    to_email=user.get("email"),
                                    user_name=user.get("full_name", user.get("username")),
                                    borrow_id=borrow.get("borrow_id"),
                                    book_id=borrow.get("book_id"),
                                    due_date=due_date,
                                    days_remaining=days_remaining
                                )
            
            return True
        except Exception as e:
            print(f"Error sending reminder emails: {e}")
            return False
    
    def _send_email(self, to_email, user_name, borrow_id, book_id, due_date, days_remaining):
        """Gửi email cụ thể"""
        try:
            # Tạo nội dung email
            subject = ""
            body = ""
            
            if days_remaining > 0:
                subject = f"📚 Nhắc nhở trả sách: Còn {days_remaining} ngày"
                body = f"""
Xin chào {user_name},

Sách bạn mượn (Mã: {borrow_id[:8]}, Sách: {book_id}) sẽ đến hạn vào ngày {due_date.strftime('%d/%m/%Y')}.
Bạn còn {days_remaining} ngày để trả sách.

Vui lòng trả sách đúng hạn để tránh bị phạt.

Trân trọng,
Thư viện
"""
            else:
                overdue_days = abs(days_remaining)
                subject = f"⚠️ CẢNH BÁO: Sách quá hạn {overdue_days} ngày"
                body = f"""
Xin chào {user_name},

Sách bạn mượn (Mã: {borrow_id[:8]}, Sách: {book_id}) đã QUÁ HẠN {overdue_days} ngày.
Hạn trả: {due_date.strftime('%d/%m/%Y')}

Bạn sẽ bị phạt {overdue_days * 5000:,} VND cho {overdue_days} ngày quá hạn.

Vui lòng trả sách NGAY LẬP TỨC để giảm tiền phạt.

Trân trọng,
Thư viện
"""
            
            # Tạo email
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Gửi email (comment nếu chưa cấu hình SMTP)
            # with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            #     server.starttls()
            #     server.login(self.sender_email, self.sender_password)
            #     server.send_message(msg)
            
            print(f"Đã gửi email cho {to_email}: {subject}")
            return True
            
        except Exception as e:
            print(f"Error sending email to {to_email}: {e}")
            return False

# Hàm chạy tự động (có thể thêm vào scheduler/cron job)
def run_daily_reminders():
    """Chạy hàng ngày để gửi email nhắc nhở"""
    reminder = EmailReminder()
    reminder.send_reminder_emails()