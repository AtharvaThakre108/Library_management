from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Book(BaseModel):
    __tablename__ = 'books'

    title = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship("Author", back_populates="books")
    isbn = Column(String(20), unique=True)
    published_date = Column(String(20))

class Author(BaseModel):
    __tablename__ = 'authors'

    name = Column(String(100), nullable=False)
    books = relationship("Book", back_populates="author")
