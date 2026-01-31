class BookAuthor:
    def __init__(self, book_id, author_id):
        self.book_id = book_id
        self.author_id = author_id

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "author_id": self.author_id
        }

    @staticmethod
    def from_dict(data: dict):
        return BookAuthor(
            book_id=data.get("book_id"),
            author_id=data.get("author_id", 0)
        )
    
    def __str__(self):
        return f"BookAuthor(book={self.book_id}, author={self.author_id})"
    
    def __repr__(self):
        return f"BookAuthor(book_id='{self.book_id}', author_id={self.author_id})"