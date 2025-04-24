from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Association table for many-to-many relationship between Client and Program
enrollment = Table(
    'enrollment',
    Base.metadata,
    Column('client_id', Integer, ForeignKey('clients.id'), primary_key=True),
    Column('program_id', Integer, ForeignKey('programs.id'), primary_key=True)
)

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Relationship
    clients = relationship("Client", secondary=enrollment, back_populates="programs")

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    contact = Column(String)
    
    # Relationship
    programs = relationship("Program", secondary=enrollment, back_populates="clients") 