from sqlalchemy.orm import Session
from . import models, schemas

def get_students(db: Session, skip: int = 0, limit: int = None):
    query = db.query(models.Student).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    student = get_student(db, student_id)
    if student:
        db.delete(student)
        db.commit()
    return student
