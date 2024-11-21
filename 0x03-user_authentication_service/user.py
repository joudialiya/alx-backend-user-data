#!/usr/bin/env python3
"""
User model module
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """User class"""
    __tablename__ = 'users'
    # id, the integer primary key
    # email, a non-nullable string
    # hashed_password, a non-nullable string
    # session_id, a nullable string
    # reset_token, a nullable string
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    reset_token = Column(String, nullable=False)
