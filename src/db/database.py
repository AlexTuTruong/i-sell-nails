"""Database Configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Nails, Base
from db.pydantic_schema import Nail

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/nails.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Creates dummy data if data does not exist"""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        dummy_nails = [
            Nail(type="Sharp", stock=10, price=0.99, sold=0),
            Nail(type="Blunt", stock=15, price=0.59, sold=0),
            Nail(type="Long", stock=15, price=1.59, sold=0),
            Nail(type="Short", stock=15, price=0.49, sold=0)
        ]

        for nail in dummy_nails:

            nail_model = Nails()
            nail_model.type = nail.type
            nail_model.stock = nail.stock
            nail_model.price = nail.price
            nail_model.sold = nail.sold
            db.add(nail_model)
        
        db.commit()
    except Exception as e:
        db.rollback()
        print("Default entries already exist")
        print(e)
    finally:
        db.close()

init_db()
