"""Defines db schema"""
from sqlalchemy import Column, Integer, PrimaryKeyConstraint, REAL, String
from db.database import Base



class Nails(Base):
    """Nail Schema"""

    __tablename__ = "nails"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, unique=True)
    stock = Column(Integer)
    price = Column(REAL)
    sold= Column(Integer)

class Ledger(Base):
    """Ledger Schema"""

    __tablename__ = "ledger" 
    nail_type = Column(String)
    price = Column(REAL)
    transaction_type = Column(String)
    total_transactions = Column(REAL)

    __table_args__ = (PrimaryKeyConstraint("nail_type", "price", "transaction_type"),)
