from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from typing import List, Optional

# Fetch a specific program by its ID
def get_program(db: Session, program_id: int):
    return db.query(models.Program).filter(models.Program.id == program_id).first()

# Fetch a program by its name
def get_program_by_name(db: Session, name: str):
    return db.query(models.Program).filter(models.Program.name == name).first()

# Get a list of all programs with optional pagination
def get_programs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Program).offset(skip).limit(limit).all()

# Create a new health program
def create_program(db: Session, program: schemas.ProgramCreate):
    db_program = models.Program(name=program.name)
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

# Delete a program if no clients are enrolled
def delete_program(db: Session, program_id: int):
    program = get_program(db, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    if len(program.clients) > 0:
        raise HTTPException(status_code=400, detail="Cannot delete program with enrolled clients")
    db.delete(program)
    db.commit()
    return {"message": "Program deleted successfully"}

# Update the details of an existing program
def update_program(db: Session, program_id: int, program_update: schemas.ProgramCreate):
    db_program = get_program(db, program_id)
    if not db_program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    for key, value in program_update.dict().items():
        setattr(db_program, key, value)
    
    db.commit()
    db.refresh(db_program)
    return db_program

# Fetch a specific client by ID
def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

# Get a list of all clients with optional pagination
def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()

# Search clients by name (case-insensitive, partial match)
def search_clients(db: Session, query: str):
    return db.query(models.Client).filter(
        models.Client.name.ilike(f"%{query}%")
    ).all()

# Register a new client
def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# Delete a client by ID
def delete_client(db: Session, client_id: int):
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"message": "Client deleted successfully"}

# Update an existing client's info
def update_client(db: Session, client_id: int, client_update: schemas.ClientCreate):
    db_client = get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    for key, value in client_update.dict().items():
        setattr(db_client, key, value)
    
    db.commit()
    db.refresh(db_client)
    return db_client

# Enroll a client into a specific health program
def enroll_client(db: Session, enrollment: schemas.EnrollmentCreate):
    client = get_client(db, enrollment.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    program = get_program(db, enrollment.program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    if program in client.programs:
        raise HTTPException(status_code=400, detail="Client already enrolled in this program")
    
    client.programs.append(program)
    db.commit()
    db.refresh(client)
    return client

# Unenroll a client from a program
def unenroll_client(db: Session, enrollment: schemas.EnrollmentCreate):
    client = get_client(db, enrollment.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    program = get_program(db, enrollment.program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    if program not in client.programs:
        raise HTTPException(status_code=400, detail="Client is not enrolled in this program")
    
    client.programs.remove(program)
    db.commit()
    db.refresh(client)
    return client
