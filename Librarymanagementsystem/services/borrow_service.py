from utils.file_handler import load_json, save_json
from datetime import datetime, timedelta
from config import MAX_BORROW_DAYS


class BorrowService:
    def __init__(
        self,
        borrow_path="data/borrow_orders.json",
        book_path="data/books.json"
    ):
        self.borrow_path = borrow_path
        self.book_path = book_path

    def borrow_book(self, user_id: int, book_id: int) -> bool:
        borrows = load_json(self.borrow_path)
        books = load_json(self.book_path)

        for book in books:
            if book["book_id"] == book_id:
                if book["available_copies"] <= 0:
                    return False
                book["available_copies"] -= 1
                break
        else:
            return False

        borrows.append({
            "user_id": user_id,
            "book_id": book_id,
            "borrow_date": datetime.now().isoformat(),
            "due_date": (datetime.now() + timedelta(days=MAX_BORROW_DAYS)).isoformat(),
            "return_date": None,
            "status": "BORROWED"
        })

        save_json(self.book_path, books)
        save_json(self.borrow_path, borrows)
        return True

    def return_book(self, user_id: int, book_id: int) -> bool:
        borrows = load_json(self.borrow_path)
        books = load_json(self.book_path)

        for borrow in borrows:
            if (
                borrow["user_id"] == user_id
                and borrow["book_id"] == book_id
                and borrow["status"] == "BORROWED"
            ):
                borrow["status"] = "RETURNED"
                borrow["return_date"] = datetime.now().isoformat()
                break
        else:
            return False

        for book in books:
            if book["book_id"] == book_id:
                book["available_copies"] += 1
                break

        save_json(self.borrow_path, borrows)
        save_json(self.book_path, books)
        return True
