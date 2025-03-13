from typing import List, Optional

from database import Database
from model import Book, Publisher, Member
from utils import logger


class Repository:
    """
    Repository class for handling database operations related to books, publishers, members, and loans.
    """

    def __init__(self) -> None:
        """Initializes the Repository class and connects to the database."""
        self.db = Database()
        try:
            self.db.connect()
        except Exception as e:
            logger.critical(f"Failed to connect to the database: {e}")
            raise RuntimeError("Database connection failed.")

    # -------------------------------------------------------------------------
    # 1. BOOK QUERIES
    # -------------------------------------------------------------------------

    def fetchall_books(self) -> List[Book]:
        """
        Fetches all books, joining with the author via the book_author join table.
        If a book has multiple authors, you might need to concatenate them.
        Here we assume one author per book for simplicity.
        """
        query = """
            SELECT b.book_id, b.title, a.name AS author, b.isbn, b.pub_year, b.genre_id, b.publisher_id
                FROM book b
                LEFT JOIN book_author ba ON b.book_id = ba.book_id
                LEFT JOIN author a ON ba.author_id = a.author_id
        """
        try:
            results = self.db.fetch_results(query=query)
            # Create Book objects assuming the Book model accepts these parameters
            return [Book(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in results]
        except Exception as e:
            logger.error(f"Failed to fetch all books: {e}")
            return []


    def add_book(self, book: Book) -> None:
        """
        Adds a new book to the 'book' table.

        Args:
            book (Book): The book object to be added.
        """
        query = """
            INSERT INTO book (title, isbn, pub_year, genre_id, publisher_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            book.title,
            book.isbn,
            book.pub_year,
            book.genre_id,
            book.publisher_id
        )
        try:
            self.db.execute_query(query=query, params=params)
            logger.info(f"Book '{book.title}' added successfully.")
        except Exception as e:
            logger.error(f"Failed to add book '{book.title}': {e}")
            raise RuntimeError("Failed to add book.")

    def delete_book_by_id(self, book_id: int) -> None:
        """
        Deletes a book by its primary key (book_id).

        Args:
            book_id (int): The ID of the book to delete.
        """
        query = "DELETE FROM book WHERE book_id = %s"
        params = (book_id,)
        try:
            self.db.execute_query(query=query, params=params)
            logger.info(f"Book with ID {book_id} deleted successfully.")
        except Exception as e:
            logger.error(f"Failed to delete book with ID {book_id}: {e}")
            raise RuntimeError("Failed to delete book.")

    def update_book(self, book: Book) -> None:
        """
        Updates the details of a book in the 'book' table.

        Args:
            book (Book): The book object with updated information.
        """
        query = """
            UPDATE book
               SET title = %s,
                   isbn = %s,
                   pub_year = %s,
                   genre_id = %s,
                   publisher_id = %s
             WHERE book_id = %s
        """
        params = (
            book.title,
            book.isbn,
            book.pub_year,
            book.genre_id,
            book.publisher_id,
            book.id  # use book.id (the model's field) which corresponds to book_id
        )
        try:
            self.db.execute_query(query=query, params=params)
            logger.info(f"Book with ID {book.id} updated successfully.")
        except Exception as e:
            logger.error(f"Failed to update book with ID {book.id}: {e}")
            raise RuntimeError("Failed to update book.")

    def list_book_by_name(self, book_name: str) -> Optional[Book]:
        """
        Fetches a book by its title.

        Args:
            book_name (str): The name of the book.

        Returns:
            Optional[Book]: The Book object if found, otherwise None.
        """
        query = """
            SELECT book_id, title, isbn, pub_year, genre_id, publisher_id
              FROM book
             WHERE title = %s
        """
        params = (book_name,)
        try:
            result = self.db.fetch_results(query=query, params=params)
            return Book(*result[0]) if result else None
        except Exception as e:
            logger.error(f"Failed to fetch book '{book_name}': {e}")
            return None

    # -------------------------------------------------------------------------
    # 2. AUTHOR-BOOK RELATIONSHIP QUERIES
    #    (To fetch books by author name using the join tables)
    # -------------------------------------------------------------------------

    def get_books_by_author(self, author_name: str) -> List[Book]:
        """
        Fetches books by the given author name.
        Uses the book_author join table and the author table.
        """
        query = """
            SELECT b.book_id,
                   b.title,
                   b.isbn,
                   b.pub_year,
                   b.genre_id,
                   b.publisher_id
              FROM book b
              JOIN book_author ba ON b.book_id = ba.book_id
              JOIN author a ON ba.author_id = a.author_id
             WHERE a.name = %s
        """
        params = (author_name,)
        try:
            results = self.db.fetch_results(query=query, params=params)
            return [Book(*row) for row in results]
        except Exception as e:
            logger.error(f"Failed to fetch books by author '{author_name}': {e}")
            return []

    def find_books_by_author_name(self, author_name: str) -> Optional[Book]:
        """
        Fetches a single book (first match) by the author's name.
        """
        query = """
            SELECT b.book_id,
                   b.title,
                   b.isbn,
                   b.pub_year,
                   b.genre_id,
                   b.publisher_id
              FROM book b
              JOIN book_author ba ON b.book_id = ba.book_id
              JOIN author a ON ba.author_id = a.author_id
             WHERE a.name = %s
             LIMIT 1
        """
        params = (author_name,)
        try:
            result = self.db.fetch_results(query=query, params=params)
            return Book(*result[0]) if result else None
        except Exception as e:
            logger.error(f"Failed to fetch book by author '{author_name}': {e}")
            return None

    # -------------------------------------------------------------------------
    # 3. PUBLISHER QUERIES
    # -------------------------------------------------------------------------

    def get_publisher(self) -> List[Publisher]:
        """
        Fetches all publishers from the 'publisher' table.

        Returns:
            List[Publisher]: A list of Publisher objects.
        """
        query = """
            SELECT publisher_id, name, address, phone, email
              FROM publisher
        """
        try:
            results = self.db.fetch_results(query=query)
            return [Publisher(*row) for row in results]
        except Exception as e:
            logger.error(f"Failed to fetch publishers: {e}")
            return []

    # -------------------------------------------------------------------------
    # 4. MEMBER QUERIES
    # -------------------------------------------------------------------------

    def get_all_members(self) -> List[Member]:
        """
        Fetches all members from the 'member' table.

        Returns:
            List[Member]: A list of Member objects.
        """
        query = """
            SELECT member_id, first_name, last_name, address, email, membership_date
              FROM members
        """
        try:
            results = self.db.fetch_results(query=query)
            return [Member(*row) for row in results]
        except Exception as e:
            logger.error(f"Failed to fetch members: {e}")
            return []

    # -------------------------------------------------------------------------
    # 5. LOAN & BORROWING QUERIES
    # -------------------------------------------------------------------------

    def list_all_loan(self) -> List[tuple]:
        """
        Fetches all loans from the 'loan' table.

        Returns:
            List[tuple]: A list of tuples containing loan information.
        """
        query = """
            SELECT loan_id,
                   copy_id,
                   member_id,
                   staff_id,
                   librarian_id,
                   issue_date,
                   due_date,
                   return_date
              FROM loan
        """
        try:
            return self.db.fetch_results(query=query)
        except Exception as e:
            logger.error(f"Failed to fetch loans: {e}")
            return []

    def list_all_members_by_book(self, book_name: str) -> List[tuple]:
        """
        Fetches all members who borrowed a specific book (by book title).

        Args:
            book_name (str): The title of the book.

        Returns:
            List[tuple]: A list of tuples containing member and loan information.
        """
        book = self.list_book_by_name(book_name)
        if not book:
            logger.warning(f"No book found with title '{book_name}'.")
            return []

        query = """
            SELECT m.first_name,
                   m.last_name,
                   b.title,
                   l.issue_date,
                   l.due_date,
                   l.return_date
              FROM members m 
              JOIN loan l ON m.member_id = l.member_id
              JOIN book_copy bc ON l.copy_id = bc.copy_id
              JOIN book b ON bc.book_id = b.book_id
             WHERE b.book_id = %s
        """
        # Use book.id from our model instead of book.book_id
        params = (book.id,)
        try:
            return self.db.fetch_results(query=query, params=params)
        except Exception as e:
            logger.error(f"Failed to fetch members for book '{book_name}': {e}")
            return []

    def list_members_borrowed_at_least_one_book(self) -> List[tuple]:
        """
        Fetches all members who have borrowed at least one book.

        Returns:
            List[tuple]: A list of tuples containing member information.
        """
        query = """
            SELECT DISTINCT m.member_id,
                            m.first_name,
                            m.last_name
              FROM members m
              JOIN loan l ON m.member_id = l.member_id
        """
        try:
            return self.db.fetch_results(query=query)
        except Exception as e:
            logger.error(f"Failed to fetch members who borrowed at least one book: {e}")
            return []
