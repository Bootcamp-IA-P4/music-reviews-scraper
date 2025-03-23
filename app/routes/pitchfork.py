from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.pitchfork import AlbumReview

router = APIRouter()

@router.get("/reviews")
def list_reviews(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    artist: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(AlbumReview)
    if artist:
        query = query.filter(AlbumReview.artist.ilike(f"%{artist}%"))
    reviews = query.offset(offset).limit(limit).all()
    return reviews
