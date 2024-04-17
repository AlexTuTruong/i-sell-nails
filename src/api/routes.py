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
    rating: int = Field(gt=-1, lt=101)
    price: float = Field(gt=-1)
    sold: int = Field(gt=-1)


@router.get("/nail_api")
def get_all_nails(db: Session = Depends(get_db)):
    """Returns all nails"""

    return db.query(models.Nails).all()


@router.get("/nail_api/{nail_id}")
def get_nail(nail_id: int, db: Session = Depends(get_db)):
    """Returns information on given nail id"""

    return db.query(models.Nails).filter(models.Nails.id == nail_id).first()


@router.get("/sold_api", response_model=float)
def get_sold_price(db: Session = Depends(get_db)):
    """Gets the price of all sold nails"""

    amount_sold = numpy.array([nail.sold for nail in db.query(models.Nails).all()])
    price_of_sold = numpy.array([nail.price for nail in db.query(models.Nails).all()])
    sold_amounts = numpy.multiply(amount_sold, price_of_sold)

    return sum(sold_amounts)


@router.post("/nail_api")
def create_nail(nail: Nail, db: Session = Depends(get_db)):
    """Makes a new nail SKU/type"""

    nail_model = models.Nails()
    nail_model.type = nail.type
    nail_model.rating = nail.rating
    nail_model.price = nail.price
    nail_model.sold = nail.sold

    db.add(nail_model)
    db.commit()

    return nail


@router.put("/nail_api/{nail_id}")
def update_nail(nail_id: int, nail: Nail, db: Session = Depends(get_db)):
    """Updates the nail values"""

    nail_model = db.query(models.Nails).filter(models.Nails.id == nail_id).first()

    if nail_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {nail_id} : Does not exist"
        )

    nail_model.type = nail.type
    nail_model.rating = nail.rating
    nail_model.price = nail.price
    nail_model.sold = nail.sold

    db.add(nail_model)
    db.commit()

    return nail


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
