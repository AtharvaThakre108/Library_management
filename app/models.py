from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True  # Ensures this class isn't used to create a table

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

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
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

class BorrowRecord(BaseModel):
    __tablename__ = 'borrow_records'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    status = Column(String(50), nullable=False, server_default="pending")  # Options: pending, approved, denied
    borrow_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime)

    user = relationship("User")
    book = relationship("Book")

class BorrowHistory(BaseModel):
    __tablename__ = 'borrow_history'

    borrow_record_id = Column(Integer, ForeignKey('borrow_records.id'), nullable=False)
    status = Column(String(50), nullable=False)  # e.g., "returned", "overdue"
    updated_at = Column(DateTime, default=func.now())
    borrow_record = relationship("BorrowRecord")

class User(BaseModel):
    __tablename__ = 'users'

    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(10), nullable=False)  # "admin" or "user"
    profile = relationship("UserProfile", back_populates="user", uselist=False)

class UserProfile(BaseModel):
    __tablename__ = 'user_profiles'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    user = relationship("User", back_populates="profile")
