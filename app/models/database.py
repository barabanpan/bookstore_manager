from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base  # ?
from sqlalchemy.orm import sessionmaker  # ?

from .. import config


db = create_engine(config.SQLALCHEMY_DATABASE_URI)
base = declarative_base()

Session = sessionmaker(db)
session = Session()
