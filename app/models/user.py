from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    username = Column(String(50), unique=True, nullable=False)
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
