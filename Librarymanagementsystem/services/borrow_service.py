from datetime import datetime, date, timedelta

from models.book import Book
from models.borrow_request import BorrowRequest
from models.borrow_order import BorrowOrder
from models.borrow_order_detail import BorrowOrderDetail
from models.member import Member
from models.fines import Fine

from utils.file_handler import read_json, write_json


class BorrowService:

    def __init__(self):
        self.books = read_json("data/book.json")
        self.users = read_json("data/user.json")
        self.requests = read_json("data/borrow_requests.json").get("borrow_requests", [])
        self.orders = read_json("data/borrow_orders.json").get("borrow_orders", [])
        self.fines = read_json("data/fine.json")

    # ================= LOADERS =================

    def _load_member(self, user_id):
        for u in self.users:
            if u["user_id"] == user_id:
                return Member(
                    u["user_id"],
                    u["username"],
                    u["password"],
                    u["email"],
                    u["full_name"],
                    u["phone_number"],
                    u["status"],
                    borrowing_limit=5,
                    penalty_status=False
                )
        return None

    def _load_book(self, book_id):
        for b in self.books:
            if b["book_id"] == book_id:
                return Book(
                    b["book_id"],
                    b["title"],
                    "",
                    b["publication_year"],
                    b["quantity"],
                    b["available_quantity"],
                    b["status"],
                    None
                )
        return None

    # ================= BORROW =================

    def create_borrow_request(self, user_id, book_id):
        new_id = len(self.requests) + 1

        req = BorrowRequest(
            request_id=new_id,
            requested_by=user_id,
            books=[book_id]
        )

        self.requests.append({
            "request_id": new_id,
            "user_id": user_id,
            "book_id": book_id,
            "status": "PENDING",
            "request_date": str(date.today())
        })

        write_json("data/borrow_requests.json", {"borrow_requests": self.requests})
        return True

    # ================= APPROVE =================

    def approve_request(self, request_id):
        for r in self.requests:
            if r["request_id"] == request_id:

                borrow_id = len(self.orders) + 1
                due = date.today() + timedelta(days=14)

                order = BorrowOrder(borrow_id, date.today(), due)
                order.add_book(r["book_id"])

                self.orders.append({
                    "borrow_id": borrow_id,
                    "user_id": r["user_id"],
                    "borrow_date": str(date.today()),
                    "due_date": str(due),
                    "status": "BORROWED",
                    "items": [{"book_id": r["book_id"], "item_status": "BORROWED"}]
                })

                r["status"] = "APPROVED"

                write_json("data/borrow_orders.json", {"borrow_orders": self.orders})
                write_json("data/borrow_requests.json", {"borrow_requests": self.requests})

                return True

        return False

    # ================= RETURN =================

    def return_book(self, borrow_id, book_id, condition="GOOD"):
        for o in self.orders:
            if o["borrow_id"] == borrow_id:
                for item in o["items"]:
                    if item["book_id"] == book_id:
                        item["item_status"] = "RETURNED"
                        item["actual_return_date"] = str(date.today())

                o["status"] = "RETURNED"
                write_json("data/borrow_orders.json", {"borrow_orders": self.orders})
                return True

        return False
