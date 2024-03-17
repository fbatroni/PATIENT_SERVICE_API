from sqlalchemy.orm import Session

from . import db_models


def get_physician(db: Session, physician_id: int):
    return db.query(db_models.Physician).filter(db_models.Physician.id == physician_id).first()

def get_physicians(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Physician).offset(skip).limit(limit).all()

