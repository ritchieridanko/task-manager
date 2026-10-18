# Task Manager Application

A full-stack mini Task Manager application built as two completely separate services (a Python FastAPI backend and a React Vite frontend), communicating solely over HTTP REST APIs.

## Repository Structure

```
task-manager/
├── backend/ <- Python FastAPI backend service, database migrations, and pytest suite
├── frontend/ <- React + Vite single-page application UI
├── compose.yaml <- Docker Compose orchestration for backend, frontend, and database
└── Makefile <- Shortcut commands to manage the full container stack
```

## Quick Start (Docker Compose)

The easiest way to run the entire application locally is by using the provided Docker Compose orchestration.

With Makefile:

1. To build and run the application:

   ```bash
   make start-app
   ```

2. To stop the application:

   ```bash
   make stop-app
   ```

Without Makefile:

1. To build and run the application:

   ```bash
   docker compose --env-file backend/.env --env-file frontend/.env up -d --build
   ```

2. To stop the application:

   ```bash
   docker compose --env-file backend/.env --env-file frontend/.env down -v
   ```

Once running:

- Frontend UI: `http://localhost:5173/`
- Backend API: `http://localhost:8000/`
- API Documentation: `http://localhost:8000/docs`
