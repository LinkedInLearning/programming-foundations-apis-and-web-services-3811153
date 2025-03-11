# Stores books in an in-memory list

class BookModel:
    books = [
        {"title": "1984", "author": "George Orwell"},
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
    ]

    @classmethod
    def get_book(cls, title):
        return next((book for book in cls.books if book["title"] == title), None)

    @classmethod
    def get_all_books(cls):
        return cls.books

    @classmethod
    def add_book(cls, title, author):
        new_book = {"title": title, "author": author}
        cls.books.append(new_book)
        return new_book
