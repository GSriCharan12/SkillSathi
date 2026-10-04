"""
SkillSathi - Database Engine and Session Management
Configured for MySQL 8+ with robust connection pooling and declarative base.
"""
import time
from typing import Generator, Tuple, Optional, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from app.config import get_settings
from app.utils.logger import logger

settings = get_settings()

db_url = settings.get_database_url()

# Configure engine with pooling parameters
try:
    if "sqlite" in db_url:
        engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False},
            echo=False
        )
    else:
        engine = create_engine(
            db_url,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_timeout=settings.DB_POOL_TIMEOUT,
            pool_recycle=settings.DB_POOL_RECYCLE,
            pool_pre_ping=True,
            echo=False
        )
except Exception as e:
    logger.warning(f"Database engine creation notice: {e}. Falling back to SQLite.")
    engine = create_engine("sqlite:///./skillsathi.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a transactional database session.
    Automatically closes session on completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_health() -> Dict[str, Any]:
    """
    Perform an active health ping to verify database connectivity, dialect, and latency.
    """
    start_time = time.time()
    try:
        is_sqlite = "sqlite" in str(engine.url)
        with engine.connect() as connection:
            if is_sqlite:
                result = connection.execute(text("SELECT 1 AS ping, sqlite_version() AS version"))
            else:
                result = connection.execute(text("SELECT 1 AS ping, VERSION() AS version"))
            row = result.fetchone()
            latency_ms = round((time.time() - start_time) * 1000, 2)
            version_str = str(row[1]) if row and len(row) > 1 else "Active"
            return {
                "status": "healthy",
                "connected": True,
                "latency_ms": latency_ms,
                "database_engine": "SQLite" if is_sqlite else "MySQL",
                "database_version": version_str,
                "host": "local" if is_sqlite else settings.MYSQL_HOST,
                "database": "skillsathi.db" if is_sqlite else settings.MYSQL_DATABASE
            }
    except SQLAlchemyError as exc:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        logger.error(f"Database health check failed: {exc}")
        return {
            "status": "degraded",
            "connected": False,
            "latency_ms": latency_ms,
            "database_engine": "SQLite" if "sqlite" in str(engine.url) else "MySQL",
            "host": settings.MYSQL_HOST,
            "database": settings.MYSQL_DATABASE,
            "error": str(exc.__cause__ or exc)
        }
    except Exception as exc:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        logger.error(f"Unexpected database connection error: {exc}")
        return {
            "status": "unhealthy",
            "connected": False,
            "latency_ms": latency_ms,
            "database_engine": "SQLite" if "sqlite" in str(engine.url) else "MySQL",
            "host": settings.MYSQL_HOST,
            "database": settings.MYSQL_DATABASE,
            "error": str(exc)
        }
