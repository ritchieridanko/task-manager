from sqlalchemy.orm import Query, Session
from typing import Optional
from uuid import UUID

from app.models.board import Board
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.board import BoardService
from app.utils import constants
from app.utils.constants import TASK_STATUSES
from app.utils.exceptions import APIException

class TaskService:
  @staticmethod
  def create_task(db: Session, board_id: UUID, payload: TaskCreate) -> Task:
    # Check if board exists
    board: Board = BoardService.get_board_by_id(db=db, board_id=board_id)
  
    new_task: Task = Task(
      board_id=board.id,
      title=payload.title,
      description=payload.description,
      status=payload.status or "TODO",
    )
  
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

  @staticmethod
  def get_tasks_by_board(db: Session, board_id: UUID, status: Optional[str] = None) -> list[Task]:
    # Check if board exists
    board: Board = BoardService.get_board_by_id(db=db, board_id=board_id)

    query: Query[Task] = db.query(Task).filter(Task.board_id == board.id)

    if status:
      s: str = status.strip().upper()
      if s not in TASK_STATUSES:
        raise APIException(
          status_code=constants.ST_CODE_400_BAD_REQUEST,
          error_code=constants.ERR_CODE_INVALID_STATUS,
          message=f"Invalid status. Must be one of {list(TASK_STATUSES)}",
        )

      query = query.filter(Task.status == s)

    return query.order_by(Task.updated_at.desc(), Task.created_at.asc()).all()

  @staticmethod
  def update_task(db: Session, task_id: UUID, payload: TaskUpdate) -> Task:
    task: Task | None = db.query(Task).filter(Task.id == task_id).first()
    if not task:
      raise APIException(
        status_code=constants.ST_CODE_404_NOT_FOUND,
        error_code=constants.ERR_CODE_TASK_NOT_FOUND,
        message=f"Task with id {task_id} does not exist",
      )

    if payload.title is not None:
      task.title = payload.title
    if payload.description is not None:
      task.description = payload.description
    if payload.status is not None:
      task.status = payload.status

    db.commit()
    db.refresh(task)
    return task

  @staticmethod
  def delete_task(db: Session, task_id: UUID) -> None:
    task: Task | None = db.query(Task).filter(Task.id == task_id).first()
    if not task:
      raise APIException(
        status_code=constants.ST_CODE_404_NOT_FOUND,
        error_code=constants.ERR_CODE_TASK_NOT_FOUND,
        message=f"Task with id {task_id} does not exist",
      )

    db.delete(task)
    db.commit()
