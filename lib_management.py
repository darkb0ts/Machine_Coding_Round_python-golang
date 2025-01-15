from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class Book:
    id: str
    title: str
    author: str
    isbn: str
    available: bool = True


@dataclass
class Member:
    id: str
    name: str
    email: str
    membership_type: str


class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
    LOST = "lost"


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, user_email: str, message: str) -> None:
        pass


class EmailNotification(NotificationService):
    def send_notification(self, user_email: str, message: str) -> None:
        # Implementation for sending email notifications
        print(f"Sending email to {user_email}: {message}")


class SMSNotification(NotificationService):
    def send_notification(self, user_email: str, message: str) -> None:
        # Implementation for sending SMS notifications
        print(f"Sending SMS to {user_email}: {message}")


class BookRepository(ABC):
    @abstractmethod
    def add_book(self, book: Book) -> None:
        pass

    @abstractmethod
    def remove_book(self, book_id: str) -> None:
        pass

    @abstractmethod
    def get_book(self, book_id: str) -> Optional[Book]:
        pass

    @abstractmethod
    def update_book_status(self, book_id: str, status: BookStatus) -> None:
        pass


class InMemoryBookRepository(BookRepository):
    def __init__(self):
        self.books: dict[str, Book] = {}

    def add_book(self, book: Book) -> None:
        self.books[book.id] = book

    def remove_book(self, book_id: str) -> None:
        if book_id in self.books:
            del self.books[book_id]

    def get_book(self, book_id: str) -> Optional[Book]:
        return self.books.get(book_id)

    def update_book_status(self, book_id: str, status: BookStatus) -> None:
        if book_id in self.books:
            self.books[book_id].available = (status == BookStatus.AVAILABLE)


class LibraryService:
    def __init__(self, book_repository: BookRepository, notification_service: NotificationService):
        self.book_repository = book_repository
        self.notification_service = notification_service
        # book_id: (member_id, due_date)
        self.borrowing_records: dict[str, tuple[str, datetime]] = {}

    def add_new_book(self, book: Book) -> None:
        self.book_repository.add_book(book)

    def borrow_book(self, book_id: str, member_id: str, member_email: str) -> bool:
        book = self.book_repository.get_book(book_id)
        if book and book.available:
            due_date = datetime.now() + timedelta(days=14)
            self.borrowing_records[book_id] = (member_id, due_date)
            self.book_repository.update_book_status(
                book_id, BookStatus.BORROWED)
            self.notification_service.send_notification(
                member_email,
                f"You have borrowed {book.title}. Due date: {due_date.date()}"
            )
            return True
        return False

    def return_book(self, book_id: str, member_id: str) -> bool:
        if book_id in self.borrowing_records:
            borrowed_member_id, _ = self.borrowing_records[book_id]
            if borrowed_member_id == member_id:
                del self.borrowing_records[book_id]
                self.book_repository.update_book_status(
                    book_id, BookStatus.AVAILABLE)
                return True
        return False

    def get_borrowed_books(self, member_id: str) -> List[Book]:
        borrowed_books = []
        for book_id, (borrowed_member_id, _) in self.borrowing_records.items():
            if borrowed_member_id == member_id:
                book = self.book_repository.get_book(book_id)
                if book:
                    borrowed_books.append(book)
        return borrowed_books

# Example usage


def main():
    # Initialize services
    book_repo = InMemoryBookRepository()
    notification_service = EmailNotification()
    library_service = LibraryService(book_repo, notification_service)

    # Add some books
    book1 = Book("1", "Clean Code", "Robert Martin", "978-0132350884")
    book2 = Book("2", "Design Patterns", "Gang of Four", "978-0201633610")
    library_service.add_new_book(book1)
    library_service.add_new_book(book2)

    # Create a member
    member = Member("M1", "John Doe", "john@example.com", "regular")

    # Borrow a book
    if library_service.borrow_book(book1.id, member.id, member.email):
        print(f"Successfully borrowed: {book1.title}")

    # Check borrowed books
    borrowed_books = library_service.get_borrowed_books(member.id)
    print(f"Borrowed books for {member.name}:")
    for book in borrowed_books:
        print(f"- {book.title}")

    # Return a book
    if library_service.return_book(book1.id, member.id):
        print(f"Successfully returned: {book1.title}")


if __name__ == "__main__":
    main()
