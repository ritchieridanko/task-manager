# Task Manager API (Backend Service)

Backend service for the mini Task Manager application, built with **Python**, **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, managed via **Alembic** migrations.

---

## 1. Prerequisites

- **Python**: `3.11+`
- **PostgreSQL**: `16+` (or running via the provided Docker Compose setup)
- **pip** (Python package manager)

---

## 2. Setup and Run Instructions

To run the service locally with virtual environment, follow the instructions below:

1. Navigate to the `backend/` directory:

   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the .env file at /backend by copying everything from .env.example, and adjust accordingly.

5. Run database migrations: (Make sure PostgreSQL is running)

   ```bash
   alembic upgrade head
   ```

6. Start the development server:

   ```bash
   python -m app.main
   # OR python3 -m app.main
   ```

7. Go to `http://localhost:8000/ping` to make sure the service is running.

## 3. Unit Testing

1. Make sure you are at `backend/` directory and have the virtual environment activated:

   ```bash
   cd backend
   source venv/bin/activate
   ```

2. Run the tests:

   ```bash
   pytest -v
   ```

## 4. API Documentation

You can review the API documentation at `http://localhost:8000/docs`. Make sure the backend service is running before you open the documentation.
