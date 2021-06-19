from .database import base, session
from sqlalchemy import Column, String, Integer, Float
from paginate_sqlalchemy import SqlalchemyOrmPage


def to_json(x):
    return {
        'id': x.id,
        'title': x.title,
        'author': x.author,
        'year': x.year,
        'price': x.price,
        'quantity': x.quantity,
        'description': x.description
    }


class BookModel(base):
    __tablename__ = 'books'

    id = Column(Integer(), primary_key=True)
    title = Column(String(255))
    author = Column(String(255))
    year = Column(Integer())
    price = Column(Float())
    quantity = Column(Integer())
    description = Column(String(1000))

    def __init__(self, title, author, year, price, quantity, description=""):
        self.title = title
        self.author = author
        self.year = year
        self.price = price
        self.quantity = quantity
        self.description = description

    def __repr__(self):
        return f"<Book '{self.title}' of {self.author} >"

    @classmethod
    def find_by_title_and_author(cls, title, author, page, limit):
        books = session.query(cls).filter(
            BookModel.title.like(f"%{title}%")).filter(
            BookModel.author.like(f"%{author}%"))
        if books:
            books = SqlalchemyOrmPage(books, page, limit).items
        return {"books": list(map(lambda x: to_json(x), books))}

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def return_all(cls):
        return session.query(cls)

    @classmethod
    def return_all_json(cls):
        return {"books": list(map(lambda x: to_json(x), session.query(cls)))}

    def update(self, title=None, author=None, year=None, price=None, quantity=None, description=None):
        if title:
            self.title = title
        if author:
            self.author = author
        if year:
            self.year = year
        if price:
            self.price = price
        if quantity:
            self.quantity = quantity
        if description:
            self.description = description
        session.commit()

    @classmethod
    def delete_by_id(cls, id):
        book = BookModel.find_by_id(id)
        session.delete(book)
        session.commit()

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = session.query(cls).delete()
            dsession.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except Exception:
            return {'message': 'Something went wrong while deleting all'}

    def save_to_db(self):
        session.add(self)
        session.commit()
