"""
SkillSathi - Base Database Model
Provides common timestamp and primary key attributes.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime
from app.database import Base


class TimeStampedBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
