# -*- coding: utf-8 -*-
from fastapi import HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from lib.response_models import PatientUpdate

from . import db_models


def get_patient(db: Session, patient_id: int):
    return db.query(db_models.Patient).filter(db_models.Patient.id == patient_id).first()


def get_patients(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    sort: str = None,
    sort_column=None,
):
    if sort is not None and sort_column is not None:
        valid_sort_options = ["desc", "asc"]
        if sort not in valid_sort_options:
            message = f"""
                Invalid sort option - cannot sort {sort}:
                Valid options are {','.join(valid_sort_options)}
                """

            raise HTTPException(
                status_code=400,
                detail=message,
            )
        # Dynamically get the column to sort by.
        sort_by = getattr(db_models.Patient, sort_column, None)
        if sort_by is None:
            # Raise HTTP exception with a 400 status code
            # and a clear error message.
            raise HTTPException(status_code=400, detail=f"Invalid sort column: {sort_column}")

        # Apply sort order.
        if sort == "asc":
            query_order_by = asc(sort_by)
        else:
            query_order_by = desc(sort_by)
        return db.query(db_models.Patient).order_by(query_order_by).offset(skip).limit(limit).all()
    return db.query(db_models.Patient).offset(skip).limit(limit).all()


def create_patient(db: Session, patient):
    # Find the physician with the least number of patients
    subquery = (
        db.query(db_models.Physician.id, func.count(db_models.Patient.id).label("patient_count"))
        .outerjoin(db_models.Patient, db_models.Physician.id == db_models.Patient.physician_id)
        .group_by(db_models.Physician.id)
        .subquery()
    )

    least_busy_physician = db.query(subquery.c.id).order_by(subquery.c.patient_count.asc()).first()

    if not least_busy_physician:
        raise HTTPException(status_code=404, detail="No physician available")

    # Create the patient with the physician_id of the least busy physician
    patient_data = patient.dict()
    patient_data["physician_id"] = least_busy_physician.id
    db_patient = db_models.Patient(**patient_data)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


# Delete - Remove a patient
def delete_patient(db: Session, patient_id: int):
    # First, check if the patient exists
    db_patient = db.query(db_models.Patient).filter(db_models.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Explicitly delete dependencies
    # Delete all related appointments
    db.query(db_models.Appointment).filter(db_models.Appointment.patient_id == patient_id).delete()

    # Delete all related prescriptions
    db.query(db_models.Prescription).filter(
        db_models.Prescription.patient_id == patient_id
    ).delete()

    # Delete all related insurance records
    db.query(db_models.Insurance).filter(db_models.Insurance.patient_id == patient_id).delete()

    # Finally, delete the patient
    db.delete(db_patient)
    db.commit()
    return {"ok": True}


# Update - Update a patient's details
def update_patient(db: Session, patient_id: int, patient: PatientUpdate):
    db_patient = db.query(db_models.Patient).filter(db_models.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for var, value in patient.dict(exclude_unset=True).items():
        setattr(db_patient, var, value)
    db.commit()
    return db_patient
