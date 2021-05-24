from .database import base, session
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import load_only
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime


class ManagerModel(base):
    __tablename__ = 'managers'

    id = Column(Integer(), primary_key=True)
    email = Column(String(255))
    name = Column(String(255))
    hash_password = Column(String(255))
    date_of_registration = Column(DateTime)

    def __init__(self, email, name, hash_password):
        self.email = email
        self.name = name
        self.hash_password = hash_password
        self.date_of_registration = datetime.now()

    def __repr__(self):
        return f"<Manager '{self.name}'>"

    @classmethod
    def find_by_email(cls, email):
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def return_all(cls):
        fields = ['email', 'name', 'date_of_registration']
        managers = session.query(cls).options(load_only(*fields)).all()
        return managers

    @classmethod
    def return_all_json(cls):
        def to_json(x):
            return {
                'id': x.id,
                'email': x.email,
                'name': x.name,
                'date_of_registration': x.date_of_registration
            }
        return {'managers': list(map(lambda x: to_json(x), session.query(cls)))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = session.query(cls).delete()
            session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except Exception:
            return {'message': 'Something went wrong while deleting all'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def save_to_db(self):
        session.add(self)
        session.commit()
