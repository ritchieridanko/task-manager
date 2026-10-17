from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.database.database import get_db
from app.schemas.board import BoardCreate, BoardResponse
from app.schemas.task import TaskCreate, TaskResponse
from app.services.board import BoardService
from app.services.task import TaskService
from app.utils import constants
from app.utils.constants import TASK_STATUSES

router: APIRouter = APIRouter(prefix="/api/boards", tags=["Boards"])

@router.post("", response_model=BoardResponse, status_code=constants.ST_CODE_201_CREATED)
def create_board(payload: BoardCreate, db: Session = Depends(get_db)) -> BoardResponse:
  return BoardService.create_board(db=db, payload=payload)

@router.get("", response_model=list[BoardResponse], status_code=constants.ST_CODE_200_OK)
def get_all_boards(db: Session = Depends(get_db)) -> list[BoardResponse]:
  return BoardService.get_all_boards(db=db)

@router.delete("/{board_id}", status_code=constants.ST_CODE_204_NO_CONTENT)
def delete_board(board_id: UUID, db: Session = Depends(get_db)) -> None:
  BoardService.delete_board(db=db, board_id=board_id)

@router.get(
  "/{board_id}/tasks",
  response_model=list[TaskResponse],
  status_code=constants.ST_CODE_200_OK,
)
def get_tasks_by_board(
  board_id: UUID,
  status: Optional[str] = Query(None, description=f"Filter tasks by status {list(TASK_STATUSES)}"),
  db: Session = Depends(get_db),
) -> list[TaskResponse]:
  return TaskService.get_tasks_by_board(db=db, board_id=board_id, status=status)

@router.post(
  "/{board_id}/tasks",
  response_model=TaskResponse,
  status_code=constants.ST_CODE_201_CREATED,
)
def create_task(
  board_id: UUID,
  payload: TaskCreate,
  db: Session = Depends(get_db),
) -> TaskResponse:
  return TaskService.create_task(db=db, board_id=board_id, payload=payload)
