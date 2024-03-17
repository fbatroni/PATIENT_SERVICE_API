from sqlalchemy.orm import Session

from . import db_models


def get_patient(db: Session, patient_id: int):
    return db.query(db_models.Patient).filter(db_models.Patient.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Patient).offset(skip).limit(limit).all()

