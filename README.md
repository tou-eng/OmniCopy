# FastAPI Campaign Management API

A simple RESTful API built with **FastAPI** and **SQLModel** to manage marketing campaigns. This project demonstrates CRUD operations, dependency injection, SQLite integration, request validation, and automatic API documentation.

## Features

- Create a campaign
- Retrieve all campaigns
- Retrieve a campaign by ID
- Update a campaign
- Delete a campaign
- SQLite database using SQLModel
- Automatic database creation
- Request validation with SQLModel
- Generic API response model
- Automatic Swagger UI documentation

## Technologies

- Python 3.13
- FastAPI
- SQLModel
- SQLAlchemy
- SQLite
- Uvicorn

## Project Structure

```
.
├── main.py
├── database.db
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows (Git Bash)

```bash
source .venv/Scripts/activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the project

```bash
fastapi dev main.py
```

or

```bash
uvicorn main:App --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```
http://127.0.0.1:8000/redoc
```

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/campaigns` | Get all campaigns |
| GET | `/campaigns/{id}` | Get campaign by ID |
| POST | `/campaigns` | Create a new campaign |
| PUT | `/campaigns/{id}` | Update a campaign |
| DELETE | `/campaigns/{id}` | Delete a campaign |

## Example Request

### Create Campaign

```http
POST /campaigns
```

```json
{
    "name": "Summer Campaign",
    "due_date": "2026-08-01T12:00:00Z"
}
```

### Response

```json
{
    "data": {
        "campaign_id": 4,
        "name": "Summer Campaign",
        "due_date": "2026-08-01T12:00:00Z",
        "created_at": "2026-07-13T15:20:00Z"
    }
}
```

## What I Learned

During this project I practiced:

- Building REST APIs with FastAPI
- CRUD operations
- SQLModel ORM
- SQLite database integration
- Dependency Injection (`Depends`)
- Database sessions
- Response models
- Generic responses using Python Generics
- Request validation
- Automatic API documentation
- HTTP status codes
- Exception handling

## Future Improvements

- JWT Authentication
- User management
- Pagination
- Filtering and sorting
- Alembic database migrations
- Docker support
- Unit testing
- PostgreSQL support

## Author

**Toufik Menaa**

- GitHub: https://github.com/tou-eng
- Portfolio: https://tou-eng.github.io/Toufik-Portfolio/

---

This project was created as part of my journey learning modern backend development with FastAPI.
