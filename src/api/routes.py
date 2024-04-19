"""Routes/API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import numpy
from . import get_db, models

router = APIRouter()

class Nail(BaseModel):
    """Nail model/Schema for pydantic validation"""

    type: str = Field(min_length=1)
    stock: int = Field(gt=-1, lt=1001)
    price: float = Field(gt=-1)
    sold: int = Field(gt=-1, lt=15)

class Ledger(BaseModel):
    """Ledger model/Schema for pydantic validation"""

    nail_type: str = Field(min_length=1)
    price: float = Field(gt=-1)
    transaction_type: str = Field()
    total_transactions: int = Field()


@router.get("/nail_api")
def get_all_nails(db: Session = Depends(get_db)):
    """Returns all nails"""

    return db.query(models.Nails).all()


@router.get("/nail_api/{nail_id}")
def get_nail(nail_id: int, db: Session = Depends(get_db)):
    """Returns information on given nail id"""

    return db.query(models.Nails).filter(models.Nails.id == nail_id).first()


@router.post("/nail_api")
def create_nail(nail: Nail, db: Session = Depends(get_db)):
    """Makes a new nail SKU/type"""

    if db.query(models.Nails).filter(models.Nails.type == nail.type).first():
        raise HTTPException(
            status_code=400, detail="Bad request: nail already exists"
        )

    nail_model = models.Nails()
    nail_model.type = nail.type
    nail_model.stock = nail.stock
    nail_model.price = nail.price
    nail_model.sold = nail.sold

    db.add(nail_model)
    db.commit()

    return nail


@router.put("/nail_api/{nail_id}/sell")
def sell_nail(nail_id: int, db: Session = Depends(get_db)):
    """Sells a nail"""

    nail_model = db.query(models.Nails).filter(models.Nails.id == nail_id).first()

    if nail_model.stock > 0:
        nail_model.stock -= 1
        nail_model.sold += 1
    else:
        raise HTTPException(
            status_code=400,
            detail=f"{nail_model.type} : has no stock!"
        )

    ledger_model = db.query(
        models.Ledger
        ).filter_by(
            nail_type=nail_model.type, price=nail_model.price, transaction_type="sell"
        ).first()

    if not ledger_model:
        ledger_model = models.Ledger()
        ledger_model.nail_type = nail_model.type
        ledger_model.price = nail_model.price
        ledger_model.transaction_type = "sell"
        ledger_model.total_transactions = 0

    ledger_model.total_transactions += 1

    db.add(nail_model)
    db.add(ledger_model)
    db.commit()


@router.put("/nail_api/{nail_id}/buyback")
def buyback_nail(nail_id: int, db: Session = Depends(get_db)):
    """Buybacks a nail"""   

    nail_model = db.query(models.Nails).filter(models.Nails.id == nail_id).first()

    if nail_model.sold > 0:
        nail_model.stock += 1
        nail_model.sold -= 1
    else:
        raise HTTPException(
            status_code=400,
            detail=f"{nail_model.type} : Cannot buy back if none sold!"
        )

    ledger_model = db.query(
        models.Ledger
        ).filter_by(
            nail_type=nail_model.type, price=nail_model.price, transaction_type="buy"
        ).first()

    if not ledger_model:
        ledger_model = models.Ledger()
        ledger_model.nail_type = nail_model.type
        ledger_model.price = nail_model.price
        ledger_model.transaction_type = "buy"
        ledger_model.total_transactions = 0

    ledger_model.total_transactions += 1

    db.add(nail_model)
    db.add(ledger_model)
    db.commit()


# @router.put("/nail_api/{nail_id}")
# def update_nail(nail_id: int, nail: Nail, db: Session = Depends(get_db)):
#     """Updates the nail values"""

#     nail_model = db.query(models.Nails).filter(models.Nails.id == nail_id).first()

#     if nail_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"ID {nail_id} : Does not exist"
#         )

#     nail_model.type = nail.type
#     nail_model.stock = nail.stock
#     nail_model.price = nail.price
#     nail_model.sold = nail.sold

#     db.add(nail_model)
#     db.commit()

#     return nail


@router.delete("/nail_api/{nail_id}")
def delete_nail(nail_id: int, db: Session = Depends(get_db)):
    """Deletes a nail given nail id"""

    nail_model = db.query(models.Nails).filter(models.Nails.id == nail_id).first()

    if nail_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {nail_id} : Does not exist"
        )

    db.query(models.Nails).filter(models.Nails.id == nail_id).delete()
    db.commit()


# @router.get("/ledger_api")
# def get_ledger(db: Session = Depends(get_db)):
#     """Returns entire ledger"""

#     return db.query(models.Ledger).all()


@router.get("/ledger_api/transactions")
def get_transactions(db: Session = Depends(get_db)):
    """Returns every type of transaction for """

    transactions = db.query(models.Ledger).all()
    if not transactions:
        raise HTTPException(
            status_code=404,
            detail="No entries in ledger"
        )

    sales, buybacks = [], []

    for entry in transactions:
        if entry.transaction_type == "sell":
            sales.append([entry.total_transactions, entry.nail_type, entry.price])
        else:
            buybacks.append([entry.total_transactions, entry.nail_type, entry.price * .75])

    return sales, buybacks


@router.delete("/ledger_api")
def reset_ledger(db: Session = Depends(get_db)):
    """Deletes all entries in Ledger table"""

    db.query(models.Ledger).delete()
    db.commit()
