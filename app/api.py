from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, models, database

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
# Program Endpoints

@router.post("/programs/", response_model=schemas.Program)
def create_program(program: schemas.ProgramCreate, db: Session = Depends(get_db)):
    db_program = crud.get_program_by_name(db, name=program.name)
    if db_program:
        raise HTTPException(status_code=400, detail="Program already exists")
    return crud.create_program(db=db, program=program)

# Get a programs
@router.get("/programs/", response_model=List[schemas.Program])
def read_programs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    programs = crud.get_programs(db, skip=skip, limit=limit)
    return programs

# Delete a program by ID
@router.delete("/programs/{program_id}")
def delete_program(program_id: int, db: Session = Depends(get_db)):
    return crud.delete_program(db=db, program_id=program_id)

# Update a program by ID
@router.put("/programs/{program_id}", response_model=schemas.Program)
def update_program(program_id: int, program: schemas.ProgramCreate, db: Session = Depends(get_db)):
    return crud.update_program(db=db, program_id=program_id, program_update=program)

# create a client
@router.post("/clients/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db=db, client=client)

# get clients
@router.get("/clients/", response_model=List[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return clients

# get a client by ID
@router.get("/clients/{client_id}", response_model=schemas.Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

# delete a client by ID
# This will delete a client and all their enrollments
@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    return crud.delete_client(db=db, client_id=client_id)

# update a client by ID
# This will update a client and all their enrollments
@router.put("/clients/{client_id}", response_model=schemas.Client)
def update_client(client_id: int, client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.update_client(db=db, client_id=client_id, client_update=client)

# search clients by name
@router.post("/clients/search/", response_model=List[schemas.Client])
def search_clients(search: schemas.ClientSearch, db: Session = Depends(get_db)):
    clients = crud.search_clients(db, query=search.query)
    return clients

# enroll a client in a program
@router.post("/enrollments/", response_model=schemas.Client)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.enroll_client(db=db, enrollment=enrollment)

# unenroll a client from a program
@router.delete("/enrollments/")
def delete_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.unenroll_client(db=db, enrollment=enrollment)