from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Env(BaseSettings):
  SERVER_HOST: str = "localhost"
  SERVER_PORT: int = 8000
  ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

  @property
  def origins(self) -> list[str]:
    return [origin.strip() for origin in self.ORIGINS.split(",")]

  model_config = SettingsConfigDict(
    env_file=os.path.abspath(
      os.path.join(os.path.dirname(__file__), "../../.env")
    ),
    env_file_encoding="utf-8",
    extra="ignore",
  )

env = Env()
