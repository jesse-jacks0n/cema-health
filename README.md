# Health Information System API

A FastAPI backend for managing health programs and client enrollments. This system allows for the creation of health programs, client registration, and program enrollment management.

## Features

- Create and manage health programs (TB, HIV, Malaria, etc.)
- Register new clients with personal information
- Enroll clients in multiple programs
- Search clients by name
- View detailed client profiles
- RESTful API with OpenAPI documentation
- SQLite database with SQLAlchemy ORM
- CORS enabled for frontend integration
- Basic unit tests

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with the following content:
   ```
   DATABASE_URL=sqlite:///./health_system.db
   SECRET_KEY=your-secret-key-for-jwt
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## Running the Application

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
2. Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

- `POST /api/v1/programs/` - Create a new health program
- `GET /api/v1/programs/` - List all programs
- `POST /api/v1/clients/` - Register a new client
- `GET /api/v1/clients/` - List all clients
- `GET /api/v1/clients/{client_id}` - Get client details
- `POST /api/v1/clients/search/` - Search clients by name
- `POST /api/v1/enrollments/` - Enroll a client in a program

## Running Tests

```bash
pytest tests/
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_api.py
├── .env
├── main.py
├── requirements.txt
└── README.md
``` 