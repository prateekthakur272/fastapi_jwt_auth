from sqlalchemy import create_engine
from config import get_settings
from sqlalchemy.orm import declarative_base, sessionmaker

settings = get_settings()
engine = create_engine(settings.DB_URL, echo=True, pool_pre_ping=True, pool_recycle=300, pool_size=5, max_overflow=0)

Base = declarative_base()
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()