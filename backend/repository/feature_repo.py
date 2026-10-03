from sqlalchemy.orm import Session
from backend.models.feature import Feature
from backend.schemas.feature_schema import FeatureCreate, FeatureUpdate
from typing import List, Optional


class FeatureRepository:
    """Repository for feature database operations."""

    @staticmethod
    def create(db: Session, feature: FeatureCreate) -> Feature:
        """Create a new feature."""
        db_feature = Feature(
            competitor_id=feature.competitor_id,
            feature_name=feature.feature_name,
            tier_available=feature.tier_available
        )
        db.add(db_feature)
        db.commit()
        db.refresh(db_feature)
        return db_feature

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Feature]:
        """Fetch all features."""
        return db.query(Feature).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, feature_id: int) -> Optional[Feature]:
        """Fetch feature by ID."""
        return db.query(Feature).filter(Feature.id == feature_id).first()

    @staticmethod
    def get_by_competitor(db: Session, competitor_id: int) -> List[Feature]:
        """Fetch all features for a competitor."""
        return db.query(Feature).filter(Feature.competitor_id == competitor_id).all()

    @staticmethod
    def get_by_competitor_and_tier(db: Session, competitor_id: int, tier: str) -> List[Feature]:
        """Fetch features by competitor and tier."""
        return db.query(Feature).filter(
            Feature.competitor_id == competitor_id,
            Feature.tier_available == tier
        ).all()

    @staticmethod
    def update(db: Session, feature_id: int, feature_update: FeatureUpdate) -> Optional[Feature]:
        """Update a feature."""
        db_feature = db.query(Feature).filter(Feature.id == feature_id).first()
        if not db_feature:
            return None
        
        update_data = feature_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_feature, key, value)
        
        db.commit()
        db.refresh(db_feature)
        return db_feature

    @staticmethod
    def delete(db: Session, feature_id: int) -> bool:
        """Delete a feature."""
        db_feature = db.query(Feature).filter(Feature.id == feature_id).first()
        if not db_feature:
            return False
        db.delete(db_feature)
        db.commit()
        return True