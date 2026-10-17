from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.configs.env import env
from app.routers import boards, tasks
from app.utils.exceptions import APIException

app: FastAPI = FastAPI(
  title="Task Manager API",
  description="Backend service for Task Manager application",
  version="1.0.0",
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=env.origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(boards.router)
app.include_router(tasks.router)

@app.exception_handler(APIException)
async def exception_handler(
  request: Request,
  err: APIException,
):
  return JSONResponse(
    status_code=err.status_code,
    content={
      "error": err.error_code,
      "message": err.message,
    },
  )

@app.get("/ping")
async def ping():
  return JSONResponse(
    status_code=200,
    content={
      "message": "API is running. Go to /docs for documentation",
    },
  )

if __name__ == "__main__":
  uvicorn.run(
    "app.main:app",
    host=env.SERVER_HOST,
    port=env.SERVER_PORT,
    reload=True,
  )
