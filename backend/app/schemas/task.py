from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from uuid import UUID

from app.utils.constants import task_statuses

class TaskCreate(BaseModel):
  title: str = Field(..., min_length=1, description="Task title is required")
  description: Optional[str] = None
  status: Optional[str] = "TODO"

  @field_validator("title")
  @classmethod
  def validate_title(cls, value: str) -> str:
    v: str = value.strip()
    if not v:
      raise ValueError("Task title must not be empty")
    return v

  @field_validator("status")
  @classmethod
  def validate_status(cls, value: Optional[str]) -> str:
    if value is None:
      return "TODO"
    v: str = value.strip().upper()
    if v not in task_statuses:
      raise ValueError(f"Invalid status. Must be one of {list(task_statuses)}")
    return v

class TaskUpdate(BaseModel):
  title: Optional[str] = None
  description: Optional[str] = None
  status: Optional[str] = None

  @field_validator("title")
  @classmethod
  def validate_title(cls, value: Optional[str]) -> Optional[str]:
    if value is not None:
      v: str = value.strip()
      if not v:
        raise ValueError("Task title must not be empty")
      return v
    return value

  @field_validator("status")
  @classmethod
  def validate_status(cls, value: Optional[str]) -> Optional[str]:
    if value is not None:
      v: str = value.strip().upper()
      if v not in task_statuses:
        raise ValueError(f"Invalid status. Must be one of {list(task_statuses)}")
      return v
    return value

class TaskResponse(BaseModel):
  id: UUID
  board_id: UUID
  title: str
  description: Optional[str] = None
  status: str
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True
