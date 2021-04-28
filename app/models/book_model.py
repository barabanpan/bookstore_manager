from .database import base, session
from sqlalchemy import Column, String, Integer


class BookModel(base):
    __tablename__ = 'books'

    id = Column(Integer(), primary_key=True)
    title = Column(String(255))
    author = Column(String(255))
    year = Column(Integer())
    description = Column(String(1000))

    def __init__(self, title, author, year, description=""):
        self.title = title
        self.author = author
        self.year = year
        self.description = description

    def __repr__(self):
        return f"<Book '{self.title}' of {self.author} >"

    @classmethod
    def find_by_title(cls, title):
        return session.query(cls).filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def return_all(cls):
        return session.query(cls)

    def update(self, title, author, year, description):
        self.title = title
        self.author = author
        self.year = year
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
