from __future__ import annotations 
from dataclasses import dataclass, field
from datetime import date 
from enum import Enum 
import uuid

class NotificationType(str, Enum): 
    SYSTEM = "system"
    DUE_DATE = "due_date"
    WAITING_LIST = "waiting_list"
    BORROW_REQUEST = "borrow_request"


@dataclass
class Notification: 
    notification_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    send_date: date = field(default_factory=date.today)
    type: NotificationType = NotificationType.SYSTEM
    user_id: int = 0
    is_sent: bool = False

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not isinstance(self.notification_id, str) or not self.notification_id.strip():
            raise ValueError("notification_id không được rỗng.")

        if not isinstance(self.content, str):
            raise ValueError("content phải là chuỗi.")

        if not isinstance(self.send_date, date):
            raise TypeError("send_date phải là kiểu datetime.date.")

        if not isinstance(self.type, NotificationType):
            raise TypeError("type phải thuộc enum NotificationType.")

        if not isinstance(self.user_id, int) or self.user_id < 0:
            raise ValueError("user_id phải là số nguyên không âm.")

        if not isinstance(self.is_sent, bool):
            raise TypeError("is_sent phải là boolean.")

    def sendNotification(self) -> str:
        self.is_sent = True
        return f"[SENT] ({self.type.value}) To user_id={self.user_id}: {self.content}"
    
    def mark_unsent(self) -> None:
        self.is_sent = False

    def update_content(self, new_content: str) -> None:
        if not isinstance(new_content, str):
            raise ValueError("new_content phải là chuỗi.")
        self.content = new_content.strip()

    def change_type(self, new_type: NotificationType) -> None:
        if not isinstance(new_type, NotificationType):
            raise TypeError("new_type phải thuộc NotificationType.")
        self.type = new_type

    def reschedule(self, new_date: date) -> None:
        if not isinstance(new_date, date):
            raise TypeError("new_date phải là datetime.date.")
        self.send_date = new_date

    def to_dict(self) -> dict:
        return {
            "notification_id": self.notification_id,
            "content": self.content,
            "send_date": self.send_date.isoformat(),
            "type": self.type.value,
            "user_id": self.user_id,
            "is_sent": self.is_sent
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            notification_id=data.get("notification_id", str(uuid.uuid4())),
            content=data.get("content", ""),
            send_date=date.fromisoformat(data.get("send_date", date.today().isoformat())),
            type=NotificationType(data.get("type", "system")),
            user_id=data.get("user_id", 0),
            is_sent=data.get("is_sent", False)
        )