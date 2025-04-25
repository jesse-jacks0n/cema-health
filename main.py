from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models, database, api
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Health Information System API",
    description="A FastAPI backend for managing health programs and client enrollments",
    version="1.0.0"
)

# Configure CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Uses environment variable or defaults to localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to CEMA Health API"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
