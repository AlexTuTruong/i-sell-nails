"""Database Initiliation"""
import db.models as models
from db.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

def get_db():
    """Gets db session"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
