from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models, database, api
from dotenv import load_dotenv

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include API routes
app.include_router(api.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
