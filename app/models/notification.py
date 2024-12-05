from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel

class Notification(BaseModel):
    __tablename__ = 'notifications'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=func.now())
    user = relationship("User")
