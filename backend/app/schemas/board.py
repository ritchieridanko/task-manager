from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from uuid import UUID

class BoardCreate(BaseModel):
  name: str = Field(..., min_length=1, description="Board name is required")

  @field_validator("name")
  @classmethod
  def validate_name(cls, value: str) -> str:
    v: str = value.strip()
    if not v:
      raise ValueError("Board name must not be empty")
    return v

class BoardResponse(BaseModel):
  id: UUID
  name: str
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)
