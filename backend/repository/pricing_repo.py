from sqlalchemy.orm import Session
from backend.models.pricing import PricingTier
from backend.schemas.pricing_schema import PricingTierCreate, PricingTierUpdate
from typing import List, Optional


class PricingRepository:
    """Repository for pricing tier database operations."""

    @staticmethod
    def create(db: Session, pricing: PricingTierCreate) -> PricingTier:
        """Create a new pricing tier."""
        db_pricing = PricingTier(
            competitor_id=pricing.competitor_id,
            tier_name=pricing.tier_name,
            price_usd=pricing.price_usd,
            billing_period=pricing.billing_period,
            description=pricing.description
        )
        db.add(db_pricing)
        db.commit()
        db.refresh(db_pricing)
        return db_pricing

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[PricingTier]:
        """Fetch all pricing tiers."""
        return db.query(PricingTier).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, pricing_id: int) -> Optional[PricingTier]:
        """Fetch pricing tier by ID."""
        return db.query(PricingTier).filter(PricingTier.id == pricing_id).first()

    @staticmethod
    def get_by_competitor(db: Session, competitor_id: int) -> List[PricingTier]:
        """Fetch all pricing tiers for a competitor."""
        return db.query(PricingTier).filter(PricingTier.competitor_id == competitor_id).all()

    @staticmethod
    def get_by_competitor_and_tier(db: Session, competitor_id: int, tier_name: str) -> Optional[PricingTier]:
        """Fetch specific pricing tier for a competitor."""
        return db.query(PricingTier).filter(
            PricingTier.competitor_id == competitor_id,
            PricingTier.tier_name == tier_name
        ).first()

    @staticmethod
    def update(db: Session, pricing_id: int, pricing_update: PricingTierUpdate) -> Optional[PricingTier]:
        """Update a pricing tier."""
        db_pricing = db.query(PricingTier).filter(PricingTier.id == pricing_id).first()
        if not db_pricing:
            return None
        
        update_data = pricing_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_pricing, key, value)
        
        db.commit()
        db.refresh(db_pricing)
        return db_pricing

    @staticmethod
    def delete(db: Session, pricing_id: int) -> bool:
        """Delete a pricing tier."""
        db_pricing = db.query(PricingTier).filter(PricingTier.id == pricing_id).first()
        if not db_pricing:
            return False
        db.delete(db_pricing)
        db.commit()
        return True