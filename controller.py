from typing import List

from model import Book
from repository import Repository
from utils import logger


class BookController:
    """
    Controller class for handling operations related to books.
    """

    def __init__(self) -> None:
        """Initializes the BookController with a repository instance."""
        self.repository = Repository()

    def getall(self) -> List[Book]:
        """
        Fetches all books from the repository.

        Returns:
            List[Book]: A list of Book objects.
        """
        try:
            return self.repository.fetchall_books()
        except Exception as e:
            logger.error(f"Failed to fetch all books: {e}")
            return []

    def add_book(self, title: str, author: str, publisher: int, isbn: str, year_published: int) -> None:
        """
        Adds a new book to the repository.
        Note: Since the book table no longer holds an author field directly,
        we assume the author relationship is handled in book_author.
        For simplicity, we add the book with a default genre_id (e.g. 1).
        """
        book = Book(
            id=0,  # Placeholder for auto-generated ID
            title=title,
            author=author,
            publisher_id=publisher,
            isbn=isbn,
            year_published=year_published,
            genre_id=1  # Default genre_id
        )
        try:
            self.repository.add_book(book=book)
            logger.info(f"Book '{title}' added successfully.")
        except Exception as e:
            logger.error(f"Failed to add book '{title}': {e}")
            raise RuntimeError("Failed to add book.")

    def update_book(self, bid: int, title: str, author: str, publisher_id: int, isbn: str, year: int) -> None:
        """
        Updates the details of a book.
        Note: The update currently modifies only the book table fields.
        If the author changes, the book_author join table should be updated accordingly.
        """
        book = Book(
            id=bid,
            title=title,
            author=author,
            publisher_id=publisher_id,
            isbn=isbn,
            year_published=year,
            genre_id=1  # Default genre_id or retrieve current genre_id as needed
        )
        try:
            self.repository.update_book(book)
            logger.info(f"Book with ID {bid} updated successfully.")
        except Exception as e:
            logger.error(f"Failed to update book with ID {bid}: {e}")
            raise RuntimeError("Failed to update book.")


class QueryController:
    """
    Controller class for handling queries related to authors, publisher, members, and loans.
    """

    def __init__(self) -> None:
        """Initializes the QueryController with a repository instance."""
        self.repository = Repository()

    def get_books_by_author_name(self, author_name: str) -> List[Book]:

        """
        Fetches books by the given author.

        Args:
            author_name (str): The name of the author.

        Returns:
            List[Book]: A list of Book objects written by the given author.
        """
        try:
            books = self.repository.get_books_by_author(author_name)
            if books is None:
                QMessageBox.warning(self, "Warning", "No books found for the given author.")
                return
            return self.repository.get_books_by_author(author_name)
        except Exception as e:
            logger.error(f"Failed to fetch books by author '{author_name}': {e}")
            return []

    def list_all_publisher(self) -> List:
        """
        Fetches all publisher from the repository.

        Returns:
            List[Publisher]: A list of Publisher objects.
        """
        try:
            return self.repository.get_publisher()
        except Exception as e:
            logger.error(f"Failed to fetch publisher: {e}")
            return []

    def get_all_members(self) -> List:
        """
        Fetches all members from the repository.

        Returns:
            List[Member]: A list of Member objects.
        """
        try:
            return self.repository.get_all_members()
        except Exception as e:
            logger.error(f"Failed to fetch members: {e}")
            return []

    def list_all_members_by_book(self, book_name: str) -> List[tuple]:
        """
        Fetches all members who have borrowed the specified book.

        Args:
            book_name (str): The title of the book.

        Returns:
            List[tuple]: A list of tuples containing member and loan information.
        """
        try:
            return self.repository.list_all_members_by_book(book_name)
        except Exception as e:
            logger.error(f"Failed to fetch members by book '{book_name}': {e}")
            return []

    def get_all_loan(self) -> List[tuple]:
        """
        Fetches all loan records from the repository.

        Returns:
            List[tuple]: A list of tuples containing loan information.
        """
        try:
            return self.repository.list_all_loan()
        except Exception as e:
            logger.error(f"Failed to fetch loan records: {e}")
            return []
        
    def list_members_borrowed_at_least_one_book(self) -> List:
        """"
        Fetches all members who have borrowed at least one book.

        Returns:
            List[Member]: A list of Member objects.
        """
        try:
            return self.repository.list_members_borrowed_at_least_one_book()
        except Exception as e:
            logger.error(f"Failed to fetch members who borrowed at least one book: {e}")
            return []
