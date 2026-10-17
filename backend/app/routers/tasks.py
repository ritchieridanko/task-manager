from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.database import get_db
from app.schemas.task import TaskResponse, TaskUpdate
from app.services.task import TaskService
from app.utils import constants

router: APIRouter = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.patch("/{task_id}", response_model=TaskResponse, status_code=constants.ST_CODE_200_OK)
def update_task(task_id: UUID, payload: TaskUpdate, db: Session = Depends(get_db)) -> TaskResponse:
  return TaskService.update_task(db=db, task_id=task_id, payload=payload)

@router.delete("/{task_id}", status_code=constants.ST_CODE_204_NO_CONTENT)
def delete_task(task_id: UUID, db: Session = Depends(get_db)) -> None:
  TaskService.delete_task(db=db, task_id=task_id)
