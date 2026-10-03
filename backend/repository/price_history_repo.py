from sqlalchemy.orm import Session
from backend.models.price_history import PriceHistory
from backend.schemas.price_history_schema import PriceHistoryCreate, PriceHistoryUpdate
from typing import List, Optional


class PriceHistoryRepository:
    """Repository for price history database operations."""

    @staticmethod
    def create(db: Session, price_history: PriceHistoryCreate) -> PriceHistory:
        """Create a new price history record."""
        db_history = PriceHistory(
            competitor_id=price_history.competitor_id,
            tier_name=price_history.tier_name,
            old_price=price_history.old_price,
            new_price=price_history.new_price
        )
        db.add(db_history)
        db.commit()
        db.refresh(db_history)
        return db_history

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[PriceHistory]:
        """Fetch all price history records."""
        return db.query(PriceHistory).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, history_id: int) -> Optional[PriceHistory]:
        """Fetch price history by ID."""
        return db.query(PriceHistory).filter(PriceHistory.id == history_id).first()

    @staticmethod
    def get_by_competitor(db: Session, competitor_id: int) -> List[PriceHistory]:
        """Fetch all price history for a competitor."""
        return db.query(PriceHistory).filter(PriceHistory.competitor_id == competitor_id).all()

    @staticmethod
    def get_by_competitor_and_tier(db: Session, competitor_id: int, tier_name: str) -> List[PriceHistory]:
        """Fetch price history by competitor and tier."""
        return db.query(PriceHistory).filter(
            PriceHistory.competitor_id == competitor_id,
            PriceHistory.tier_name == tier_name
        ).all()

    @staticmethod
    def update(db: Session, history_id: int, history_update: PriceHistoryUpdate) -> Optional[PriceHistory]:
        """Update price history record."""
        db_history = db.query(PriceHistory).filter(PriceHistory.id == history_id).first()
        if not db_history:
            return None
        
        update_data = history_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_history, key, value)
        
        db.commit()
        db.refresh(db_history)
        return db_history

    @staticmethod
    def delete(db: Session, history_id: int) -> bool:
        """Delete price history record."""
        db_history = db.query(PriceHistory).filter(PriceHistory.id == history_id).first()
        if not db_history:
            return False
        db.delete(db_history)
        db.commit()
        return True