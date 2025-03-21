from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.pitchfork import AlbumReview

router = APIRouter()

@router.get("/reviews")
def list_reviews(db: Session = Depends(get_db)):
    reviews = db.query(AlbumReview).all()
    return reviews
