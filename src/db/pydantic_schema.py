"""Pydantic schemas"""
from pydantic import BaseModel, Field

class Nail(BaseModel):
    """Nail Schema for pydantic validation"""

    type: str = Field(min_length=1)
    stock: int = Field(gt=-1, lt=1001)
    price: float = Field(gt=-1)
    sold: int = Field(gt=-1, lt=15)

class Ledger(BaseModel):
    """Ledger Schema for pydantic validation"""

    nail_type: str = Field(min_length=1)
    price: float = Field(gt=-1)
    transaction_type: str = Field()
    total_transactions: int = Field()
