from sqlalchemy.orm import Session
from models.competitor import Competitor
from schemas.competitor_schema import CompetitorCreate, CompetitorUpdate

class CompetitorRepository:
    @staticmethod
    def create(db: Session, competitor: CompetitorCreate):
        db_competitor = Competitor(**competitor.dict())
        db.add(db_competitor)
        db.commit()
        db.refresh(db_competitor)
        return db_competitor
    
    @staticmethod
    def get(db: Session, competitor_id: int):
        return db.query(Competitor).filter(Competitor.id == competitor_id).first()
    
    @staticmethod
    def get_all(db: Session, limit: int = 100):
        return db.query(Competitor).limit(limit).all()
    
    @staticmethod
    def update(db: Session, competitor_id: int, competitor: CompetitorUpdate):
        db_competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
        if db_competitor:
            update_data = competitor.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_competitor, key, value)
            db.commit()
            db.refresh(db_competitor)
        return db_competitor
    
    @staticmethod
    def delete(db: Session, competitor_id: int):
        db_competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
        if db_competitor:
            db.delete(db_competitor)
            db.commit()
        return db_competitor

competitor_repo = CompetitorRepository()
