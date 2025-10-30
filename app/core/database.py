from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# engine
engine = create_engine(DATABASE_URL)

# session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# base model for ORM
Base = declarative_base()
