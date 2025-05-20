from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://34.133.31.90:5173"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

@app.get("/students/", response_model=list[schemas.Student])
def read_students(skip: int = 0, limit: int | None = None, db: Session = Depends(get_db)):
    return crud.get_students(db, skip=skip, limit=limit)

@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.delete("/students/{student_id}", response_model=schemas.Student)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.delete_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
