"""Defines db schema"""
from db.database import Base
from sqlalchemy import Column, Integer, REAL, String



class Nails(Base):
    """Nail Schema"""

    __tablename__ = "nails"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    rating = Column(Integer)
    price = Column(REAL)
    sold= Column(Integer)
