from sqlalchemy import Column, String, Integer, Identity, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, Identity(start=1), primary_key=True)
    name = Column(String)
    birth_year = Column(Integer)

    books = relationship('Book', back_populates='author')


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, Identity(start=1), primary_key=True)
    title = Column(String)
    release_year = Column(Integer)

    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship('Author', back_populates='books')
