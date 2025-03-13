from typing import Tuple

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox
)

from controller import BookController
from utils import logger


class BookTab(QWidget):
    """Tab widget for managing books, including adding, updating, and deleting book records."""

    def __init__(self) -> None:
        """Initialize the BookTab and set up the UI."""
        super().__init__()
        self.controller = BookController()
        self.init_ui()
        self.refresh_book_table()

    def init_ui(self) -> None:
        """Set up the UI components, including form fields, buttons, and the book table."""
        self.main_layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.setStyleSheet(self.get_stylesheet())
        self.create_form_fields()
        self.create_buttons()
        self.setup_books_table()

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.books_table)
        self.setLayout(self.main_layout)

    def get_stylesheet(self) -> str:
        """Return the stylesheet for styling the form and table."""
        return """
            /* Bold labels with a slightly refined font */
            QLabel {
                font-size: 14px;
                color: #333;
                font-weight: bold;
            }

            /* Line edits with a subtle background */
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
                background: #f9f9f9;
            }
            QLineEdit:focus {
                background-color: #e6f7ff;
                border-color: #80bdff;
            }

            /* Material Design Flat Dark Purple Buttons */
            QPushButton {
                background-color: #6A0DAD;   /* Dark purple */
                color: white;
                border: none;
                border-radius: 0;            /* Flat design with no rounded corners */
                padding: 5px 10px;           /* Smaller button size */
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a009e;   /* Slightly darker shade on hover */
            }

            /* Table styling for a clean and modern look */
            QTableWidget {
                border: 1px solid #ddd;
                font-size: 13px;
                background: #fff;
                gridline-color: #ccc;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }

            /* Table header styling with bold text */
            QHeaderView::section {
                background-color: #f1f1f1;
                padding: 8px;
                border: 1px solid #ddd;
                font-size: 13px;
                font-weight: bold;
            }
        """

    def create_form_fields(self) -> None:
        """Create form fields for book details: Title, Author, Publisher, ISBN, and Year."""
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.publisher_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.year_published_input = QLineEdit()

        self.form_layout.addRow(QLabel("Title:"), self.title_input)
        self.form_layout.addRow(QLabel("Author:"), self.author_input)
        self.form_layout.addRow(QLabel("Publisher:"), self.publisher_input)
        self.form_layout.addRow(QLabel("ISBN:"), self.isbn_input)
        self.form_layout.addRow(QLabel("Year:"), self.year_published_input)

    def create_buttons(self) -> None:
        """Create buttons for adding, updating, and deleting books."""
        self.button_layout = QHBoxLayout()
        self.add_book_button = QPushButton("Add Book")
        self.update_book_button = QPushButton("Update Book")
        self.delete_book_button = QPushButton("Delete Book")

        self.add_book_button.clicked.connect(self.add_book)
        self.update_book_button.clicked.connect(self.update_book)
        self.delete_book_button.clicked.connect(self.delete_book)

        self.button_layout.addWidget(self.add_book_button)
        self.button_layout.addWidget(self.update_book_button)
        self.button_layout.addWidget(self.delete_book_button)

    def setup_books_table(self) -> None:
        """Set up the book table for displaying book records."""
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(6)
        self.books_table.setHorizontalHeaderLabels(["Book ID", "Title", "Author", "Publisher ID", "ISBN", "Year"])
        self.books_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.books_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.books_table.horizontalHeader().setStretchLastSection(True)

    def refresh_book_table(self) -> None:
        """Refresh the book table with the latest records from the database."""
        try:
            self.books_table.setRowCount(0)
            books = self.controller.getall()

            for book_index, book in enumerate(books):
                self.books_table.insertRow(book_index)
                self.books_table.setItem(book_index, 0, QTableWidgetItem(str(book.id)))
                self.books_table.setItem(book_index, 1, QTableWidgetItem(book.title))
                self.books_table.setItem(book_index, 2, QTableWidgetItem(book.author))
                self.books_table.setItem(book_index, 3, QTableWidgetItem(str(book.publisher_id)))
                self.books_table.setItem(book_index, 4, QTableWidgetItem(book.isbn))
                self.books_table.setItem(book_index, 5, QTableWidgetItem(str(book.year_published)))
        except Exception as e:
            logger.critical(f"Failed to refresh the book table: {e}")
            QMessageBox.critical(self, "Error", "Failed to retrieve books. Check the logs for details.")

    def add_book(self) -> None:
        """Add a new book using the form input."""
        title, author, publisher, isbn, year = self.get_form_input()
        if not title or not author:
            QMessageBox.warning(self, "Validation Error", "Title and Author are required fields.")
            return

        try:
            year = int(year)
            publisher_id = int(publisher)
            # Assume a default genre_id (e.g. 1) since the form does not include it.
            self.controller.add_book(title, author, publisher_id, isbn, year)

            # Clear form fields
            self.title_input.clear()
            self.author_input.clear()
            self.publisher_input.clear()
            self.isbn_input.clear()
            self.year_published_input.clear()

            QMessageBox.information(self, "Success", "Book added successfully!")
            self.refresh_book_table()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Year and Publisher must be integers.")
        except Exception as e:
            logger.error(f"Failed to add book: {e}")
            QMessageBox.critical(self, "Error", "Failed to add a new book. Check the logs for details.")

    def update_book(self) -> None:
        """Update the selected book with the new values from the form."""
        selected_items = self.books_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a book to update.")
            return

        book_id = int(selected_items[0].text())
        book_title, book_author, book_publisher_id, book_isbn, book_year = (
            selected_items[1].text(),
            selected_items[2].text(),
            selected_items[3].text(),
            selected_items[4].text(),
            selected_items[5].text(),
        )

        title, author, publisher, isbn, year = self.get_form_input()

        if title:
            book_title = title
        if author:
            book_author = author
        if publisher:
            book_publisher_id = publisher
        if isbn:
            book_isbn = isbn
        if year:
            book_year = year

        try:
            # Convert publisher and year to integers as needed
            book_publisher_id = int(book_publisher_id)
            book_year = int(book_year)

            self.controller.update_book(book_id, book_title, book_author, book_publisher_id, book_isbn, book_year)

            self.title_input.clear()
            self.author_input.clear()
            self.publisher_input.clear()
            self.isbn_input.clear()
            self.year_published_input.clear()

            QMessageBox.information(self, "Success", "Book updated successfully!")
            self.refresh_book_table()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Year and Publisher must be integers.")
        except Exception as e:
            logger.error(f"Failed to update book {book_id}: {e}")
            QMessageBox.critical(self, "Error", f"Failed to update the book. Check the logs for details.")

    def delete_book(self) -> None:
        """Delete the selected book after user confirmation."""
        selected_items = self.books_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a book to delete.")
            return

        book_id = int(selected_items[0].text())
        book_title = selected_items[1].text()

        confirmation = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete the book '{book_title}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmation == QMessageBox.No:
            return

        try:
            self.controller.delete_by_id(book_id)

            self.title_input.clear()
            self.author_input.clear()
            self.publisher_input.clear()
            self.isbn_input.clear()
            self.year_published_input.clear()
        
            QMessageBox.information(self, "Success", "Book deleted successfully!")
            self.refresh_book_table()
        except Exception as e:
            logger.error(f"Failed to delete book {book_id}: {e}")
            QMessageBox.critical(self, "Error", f"Failed to delete the book. Check the logs for details.")

    def get_form_input(self) -> Tuple[str, str, str, str, str]:
        """Get and return the form input as a tuple of strings."""
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        publisher = self.publisher_input.text().strip()
        isbn = self.isbn_input.text().strip()
        year = self.year_published_input.text().strip()
        return title, author, publisher, isbn, year
