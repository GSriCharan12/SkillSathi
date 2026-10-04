"""
SkillSathi - Generic Base Repository
Encapsulates all standard CRUD operations with SQLAlchemy session management.
"""
from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from app.models.base import TimeStampedBase

ModelT = TypeVar("ModelT", bound=TimeStampedBase)


class BaseRepository(Generic[ModelT]):
    """Generic repository providing clean database abstraction layer."""

    def __init__(self, model: Type[ModelT], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, item_id: int) -> Optional[ModelT]:
        return self.db.query(self.model).filter(self.model.id == item_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelT]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, item: ModelT) -> ModelT:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item_id: int, update_data: dict[str, Any]) -> Optional[ModelT]:
        db_item = self.get_by_id(item_id)
        if not db_item:
            return None
        for field, value in update_data.items():
            if hasattr(db_item, field):
                setattr(db_item, field, value)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, item_id: int) -> bool:
        db_item = self.get_by_id(item_id)
        if not db_item:
            return False
        self.db.delete(db_item)
        self.db.commit()
        return True
