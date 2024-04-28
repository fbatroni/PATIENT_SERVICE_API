""" Responsible for creating the Database Models
# SQLAlchemy uses the term "model" to refer to these classes
# and instances that interact with the database.
"""

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from .database_connection import Base

# Note:
# SQLAlchemy models define attributes
# using =, and pass the type as a parameter to Column
# i.e name = Column(String)


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    ssn = Column(String, nullable=False)
    position = Column(String)
    hospital_id = Column(Integer, ForeignKey("hospital.id"))
    department_id = Column(Integer, ForeignKey("department.id"))


class Physician(Employee):
    __tablename__ = "physician"
    id = Column(Integer, ForeignKey("employee.id"))
    specialty = Column(String)
    patients = relationship("Patient", backref="physician")


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    ssn = Column(String, nullable=False)
    gender = Column(String)
    address = Column(String)
    physician_id = Column(Integer, ForeignKey("physician.id"))
    insurances = relationship("Insurance", backref="patient")


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospital.id"))


class Prescription(Base):
    __tablename__ = "prescription"
    id = Column(Integer, primary_key=True)
    prescription_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    dosage = Column(String)
    frequency = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    refills_available = Column(Integer, nullable=False, default=0)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    medication_id = Column(Integer, ForeignKey("medication.id"))
    prescribing_physician_id = Column(Integer, ForeignKey("physician.id"))


class Medication(Base):
    __tablename__ = "medication"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    description = Column(String)


class Insurance(Base):
    __tablename__ = "insurance"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    provider_name = Column(String, nullable=False)
    policy_number = Column(String, nullable=False)


class Hospital(Base):
    __tablename__ = "hospital"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)


class Appointment(Base):
    __tablename__ = "appointment"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    physician_id = Column(Integer, ForeignKey("physician.id"))
    description = Column(String)
    appointment_date = Column(Date, nullable=False)
