import pytest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker
from uuid import UUID, uuid4

from app.database.database import base
from app.models.board import Board
from app.models.task import Task
from app.schemas.board import BoardCreate
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.board import BoardService
from app.services.task import TaskService
from app.utils.constants import TASK_STATUSES
from app.utils.exceptions import APIException

@pytest.fixture(scope="function")
def session():
  engine: Engine = create_engine(
    "sqlite:///:memory:",
    connect_args={
      "check_same_thread": False,
    },
  )

  testing_session_local: sessionmaker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
  )

  base.metadata.create_all(bind=engine)
  session = testing_session_local()

  try:
    yield session
  finally:
    session.close()
    base.metadata.drop_all(bind=engine)

# SUCCESS TESTS

def test_create_board_success(session: Session):
  board: Board = BoardService.create_board(
    db=session,
    payload=BoardCreate(name="Board 1"),
  )

  assert board.name == "Board 1"

def test_get_all_boards_success(session: Session):
  BoardService.create_board(
    db=session,
    payload=BoardCreate(name="Board 1"),
  )
  BoardService.create_board(
    db=session,
    payload=BoardCreate(name="Board 2"),
  )

  boards: list[Board] = BoardService.get_all_boards(db=session)

  assert len(boards) == 2
  assert boards[0].name == "Board 1"
  assert boards[1].name == "Board 2"

def test_get_board_by_id_success(session: Session):
  new_board: Board = BoardService.create_board(
    db=session,
    payload=BoardCreate(name="Board 1"),
  )

  board: Board = BoardService.get_board_by_id(db=session, board_id=new_board.id)

  assert board.id == new_board.id
  assert board.name == new_board.name
  assert board.created_at == new_board.created_at
  assert board.updated_at == new_board.updated_at

def test_delete_board_success(session: Session):
  BoardService.create_board(
    db=session,
    payload=BoardCreate(name="Board 1"),
  )

  boards: list[Board] = BoardService.get_all_boards(db=session)

  assert len(boards) == 1

  BoardService.delete_board(db=session, board_id=boards[0].id)

  boards = BoardService.get_all_boards(db=session)

  assert len(boards) == 0

def test_create_task_success(session: Session):
  board: Board = BoardService.create_board(
    db=session,
    payload=BoardCreate(name="Board 1"),
  )

  task: Task = TaskService.create_task(
    db=session,
    board_id=board.id,
    payload=TaskCreate(title="Task 1", status="TODO"),
  )

  assert task.board_id == board.id
  assert task.title == "Task 1"
  assert task.description is None
  assert task.status == "TODO"

def test_get_tasks_by_board_success(session: Session):
  board: Board = BoardService.create_board(
    db=session,
    payload=BoardCreate(name="Board 1"),
  )

  TaskService.create_task(
    db=session,
    board_id=board.id,
    payload=TaskCreate(title="Task 1", status="TODO"),
  )
  TaskService.create_task(
    db=session,
    board_id=board.id,
    payload=TaskCreate(title="Task 2", status="TODO"),
  )
  TaskService.create_task(
    db=session,
    board_id=board.id,
    payload=TaskCreate(title="Task 3", status="IN_PROGRESS"),
  )
  
  tasks: list[Task] = TaskService.get_tasks_by_board(db=session, board_id=board.id, status="TODO")

  assert len(tasks) == 2
  assert tasks[0].status == "TODO"
  assert tasks[1].status == "TODO"

def test_update_task_success(session: Session):
  board: Board = BoardService.create_board(
    db=session,
    payload=BoardCreate(name="Board 1"),
  )
  
  task: Task = TaskService.create_task(
    db=session,
    board_id=board.id,
    payload=TaskCreate(title="Task 1", status="TODO"),
  )

  updated_task: Task = TaskService.update_task(
    db=session,
    task_id=task.id,
    payload=TaskUpdate(
      title="Task 2",
      status="IN_PROGRESS",
    ),
  )

  assert updated_task.id == task.id
  assert updated_task.title == "Task 2"
  assert updated_task.status == "IN_PROGRESS"

def test_delete_task_success(session: Session):
  board: Board = BoardService.create_board(
    db=session,
    payload=BoardCreate(name="Board 1"),
  )

  TaskService.create_task(
    db=session,
    board_id=board.id,
    payload=TaskCreate(title="Task 1"),
  )

  tasks: list[Task] = TaskService.get_tasks_by_board(db=session, board_id=board.id)

  assert len(tasks) == 1

  TaskService.delete_task(db=session, task_id=tasks[0].id)

  tasks = TaskService.get_tasks_by_board(db=session, board_id=board.id)

  assert len(tasks) == 0

# FAILURE TESTS

def test_create_board_no_name():
  with pytest.raises(ValueError):
    BoardCreate()

def test_create_board_empty_name():
  with pytest.raises(ValueError):
    BoardCreate(name="")

def test_create_board_whitespace_name():
  with pytest.raises(ValueError):
    BoardCreate(name="   ")

def test_get_nonexistent_board(session: Session):
  fake_board_id: UUID = uuid4()

  with pytest.raises(APIException) as exc_info:
    BoardService.get_board_by_id(db=session, board_id=fake_board_id)
  
  assert exc_info.value.status_code == 404
  assert exc_info.value.error_code == "BOARD_NOT_FOUND"
  assert exc_info.value.message == f"Board with id {fake_board_id} does not exist"

def test_delete_nonexistent_board(session: Session):
  fake_board_id: UUID = uuid4()
  
  with pytest.raises(APIException) as exc_info:
    BoardService.delete_board(db=session, board_id=fake_board_id)
  
  assert exc_info.value.status_code == 404
  assert exc_info.value.error_code == "BOARD_NOT_FOUND"
  assert exc_info.value.message == f"Board with id {fake_board_id} does not exist"

def test_delete_board_with_tasks(session: Session):
  board: Board = BoardService.create_board(
    db=session,
    payload=BoardCreate(name="Board 1"),
  )

  TaskService.create_task(
    db=session,
    board_id=board.id,
    payload=TaskCreate(title="Task 1"),
  )

  with pytest.raises(APIException) as exc_info:
    BoardService.delete_board(db=session, board_id=board.id)
    
  assert exc_info.value.status_code == 400
  assert exc_info.value.error_code == "BOARD_NOT_EMPTY"
  assert exc_info.value.message == "Unable to delete board with tasks"

def test_create_task_no_title():
  with pytest.raises(ValueError):
    TaskCreate()

def test_create_task_empty_title():
  with pytest.raises(ValueError):
    TaskCreate(title="")

def test_create_task_whitespace_title():
  with pytest.raises(ValueError):
    TaskCreate(title="   ")

def test_create_task_invalid_status():
  with pytest.raises(ValueError):
    TaskCreate(title="Task 1", status="CANCELLED")

def test_create_task_nonexistent_board(session: Session):
  fake_board_id: UUID = uuid4()

  with pytest.raises(APIException) as exc_info:
    TaskService.create_task(
      db=session,
      board_id=fake_board_id,
      payload=TaskCreate(title="Task 1"),
    )

  assert exc_info.value.status_code == 404
  assert exc_info.value.error_code == "BOARD_NOT_FOUND"
  assert exc_info.value.message == f"Board with id {fake_board_id} does not exist"

def test_get_tasks_by_nonexistant_board(session: Session):
  fake_board_id: UUID = uuid4()
  
  with pytest.raises(APIException) as exc_info:
    TaskService.get_tasks_by_board(
      db=session,
      board_id=fake_board_id,
    )
  
  assert exc_info.value.status_code == 404
  assert exc_info.value.error_code == "BOARD_NOT_FOUND"
  assert exc_info.value.message == f"Board with id {fake_board_id} does not exist"

def test_get_tasks_with_invalid_status(session: Session):
  board: Board = BoardService.create_board(
    db=session,
    payload=BoardCreate(name="Board 1"),
  )

  TaskService.create_task(
    db=session,
    board_id=board.id,
    payload=TaskCreate(title="Task 1"),
  )

  with pytest.raises(APIException) as exc_info:
    TaskService.get_tasks_by_board(
      db=session,
      board_id=board.id,
      status="CANCELLED",
    )
  
  assert exc_info.value.status_code == 400
  assert exc_info.value.error_code == "INVALID_STATUS"
  assert exc_info.value.message == f"Invalid status. Must be one of {list(TASK_STATUSES)}"

def test_update_task_empty_title():
  with pytest.raises(ValueError):
    TaskUpdate(title="")

def test_update_task_whitespace_title():
  with pytest.raises(ValueError):
    TaskUpdate(title="   ")

def test_update_task_invalid_status():
  with pytest.raises(ValueError):
    TaskUpdate(status="CANCELLED")

def test_update_nonexistent_task(session: Session):
  fake_task_id: UUID = uuid4()
  
  with pytest.raises(APIException) as exc_info:
    TaskService.update_task(
      db=session,
      task_id=fake_task_id,
      payload=TaskUpdate(status="DONE"),
    )
  
  assert exc_info.value.status_code == 404
  assert exc_info.value.error_code == "TASK_NOT_FOUND"
  assert exc_info.value.message == f"Task with id {fake_task_id} does not exist"

def test_delete_nonexistent_task(session: Session):
  fake_task_id: UUID = uuid4()
    
  with pytest.raises(APIException) as exc_info:
    TaskService.delete_task(
      db=session,
      task_id=fake_task_id,
    )
    
  assert exc_info.value.status_code == 404
  assert exc_info.value.error_code == "TASK_NOT_FOUND"
  assert exc_info.value.message == f"Task with id {fake_task_id} does not exist"
