from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.recommended_service import get_recommended_reviews

router = APIRouter()

@router.get("/recommended_reviews")
def recommended_reviews(user_id: str = "test_user", db: Session = Depends(get_db)):
    recommended = get_recommended_reviews(user_id, db)
    return recommended