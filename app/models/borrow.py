from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel

class BorrowRecord(BaseModel):
    __tablename__ = 'borrow_records'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    status = Column(String(50), nullable=False, default="pending")  # Options: pending, approved, denied
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
