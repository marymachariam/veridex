from sqlalchemy.orm import Session
from backend.models.review import Review
from backend.schemas.review_schema import ReviewCreate, ReviewUpdate
from typing import List, Optional


class ReviewRepository:
    """Repository for review database operations."""

    @staticmethod
    def create(db: Session, review: ReviewCreate) -> Review:
        """Create a new review."""
        db_review = Review(
            competitor_id=review.competitor_id,
            source=review.source,
            rating=review.rating,
            sentiment=review.sentiment,
            comment_summary=review.comment_summary
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Review]:
        """Fetch all reviews."""
        return db.query(Review).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, review_id: int) -> Optional[Review]:
        """Fetch review by ID."""
        return db.query(Review).filter(Review.id == review_id).first()

    @staticmethod
    def get_by_competitor(db: Session, competitor_id: int) -> List[Review]:
        """Fetch all reviews for a competitor."""
        return db.query(Review).filter(Review.competitor_id == competitor_id).all()

    @staticmethod
    def get_by_competitor_and_source(db: Session, competitor_id: int, source: str) -> List[Review]:
        """Fetch reviews by competitor and source."""
        return db.query(Review).filter(
            Review.competitor_id == competitor_id,
            Review.source == source
        ).all()

    @staticmethod
    def get_by_sentiment(db: Session, sentiment: str) -> List[Review]:
        """Fetch reviews by sentiment."""
        return db.query(Review).filter(Review.sentiment == sentiment).all()

    @staticmethod
    def update(db: Session, review_id: int, review_update: ReviewUpdate) -> Optional[Review]:
        """Update a review."""
        db_review = db.query(Review).filter(Review.id == review_id).first()
        if not db_review:
            return None
        
        update_data = review_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_review, key, value)
        
        db.commit()
        db.refresh(db_review)
        return db_review

    @staticmethod
    def delete(db: Session, review_id: int) -> bool:
        """Delete a review."""
        db_review = db.query(Review).filter(Review.id == review_id).first()
        if not db_review:
            return False
        db.delete(db_review)
        db.commit()
        return True