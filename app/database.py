
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
 
DATABASE_URL = "sqlite:///./items.db"
 
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # required for SQLite
)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
 
class Base(DeclarativeBase):
    pass
 
 
def get_db():
    """Dependency that provides a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()