from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Env(BaseSettings):
  SERVER_HOST: str = "localhost"
  SERVER_PORT: int = 8000
  ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
  
  DATABASE_HOST: str = "localhost"
  DATABASE_PORT: int = 5432
  DATABASE_USER: str = "postgres"
  DATABASE_PASS: str = "postgres"
  DATABASE_NAME: str = "task_manager_db"

  @property
  def origins(self) -> list[str]:
    return [origin.strip() for origin in self.ORIGINS.split(",")]

  @property
  def database_url(self) -> str:
    return f"postgresql+psycopg://{self.DATABASE_USER}:{self.DATABASE_PASS}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
  
  model_config = SettingsConfigDict(
    env_file=os.path.abspath(
      os.path.join(os.path.dirname(__file__), "../../.env")
    ),
    env_file_encoding="utf-8",
    extra="ignore",
  )

env = Env()
