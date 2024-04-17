"""Defines db schema"""
from sqlalchemy import Column, Integer, REAL, String
from db.database import Base



class Nails(Base):
    """Nail Schema"""

    __tablename__ = "nails"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    rating = Column(Integer)
    price = Column(REAL)
    sold= Column(Integer)
