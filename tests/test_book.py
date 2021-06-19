import pytest

from app.models.book_model import BookModel


book_id = 0

@pytest.fixture
def book():
    return BookModel(
        title="Cool Book",
        author="James Cool",
        year="2021",
        price=100,
        quantity=56,
        description="Cool book by a cool author"
    )



def test_add_book(book):
    book.save_to_db()
    global book_id
    book_id = book.id

    assert isinstance(book_id, int)

    book_from_db = BookModel.find_by_id(book_id)

    assert book_from_db
    assert book_from_db.title == book.title



def test_update_book():
    book_from_db = BookModel.find_by_id(book_id)
    book_from_db.update(title="New Cooler Title")

    updated_book = BookModel.find_by_id(book_id)
    assert updated_book.title == "New Cooler Title"


def test_delete_book():
    BookModel.delete_by_id(book_id)
    book = BookModel.find_by_id(book_id)

    assert not book
