from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment or fallback to local SQLite DB
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./health_system.db")

# Create SQLAlchemy engine (special flag needed for SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# creating ORM models
Base = declarative_base()

# Dependency function for FastAPI routes to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide the DB session
    finally:
        db.close()  