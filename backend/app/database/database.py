from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.configs.env import env

engine: Engine = create_engine(url=env.database_url)

session_local: sessionmaker = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine,
)

base = declarative_base()

def get_db():
  db = session_local()
  try:
    yield db
  finally:
    db.close()
