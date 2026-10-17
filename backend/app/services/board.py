from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.board import Board
from app.models.task import Task
from app.schemas.board import BoardCreate
from app.utils import constants
from app.utils.exceptions import APIException

class BoardService:
  @staticmethod
  def create_board(db: Session, payload: BoardCreate) -> Board:
    new_board: Board = Board(name=payload.name)
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

  @staticmethod
  def get_all_boards(db: Session) -> list[Board]:
    return db.query(Board).order_by(Board.created_at.asc()).all()

  @staticmethod
  def get_board_by_id(db: Session, board_id: UUID) -> Board:
    board: Board | None = db.query(Board).filter(Board.id == board_id).first()
    if not board:
      raise APIException(
        status_code=404,
        error_code=constants.err_code_board_not_found,
        message=f"Board with id {board_id} does not exist",
      )
    return board

  @staticmethod
  def delete_board(db: Session, board_id: UUID) -> None:
    board: Board = BoardService.get_board_by_id(db=db, board_id=board_id)

    # Check if board still has any tasks
    task_count: int = db.query(Task).filter(Task.board_id == board.id).count()
    if task_count > 0:
      raise APIException(
        status_code=400,
        error_code=constants.err_code_board_not_empty,
        message="Unable to delete board with tasks",
      )

    db.delete(board)
    try:
      db.commit()
    except IntegrityError:
      db.rollback()

      raise APIException(
        status_code=400,
        error_code=constants.err_code_delete_restricted,
        message="Unable to delete board with tasks",
      )
