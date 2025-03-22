from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.recommended_service import get_recommended_reviews
from app.services import user_service

router = APIRouter()

@router.get("/recommended_reviews")
def recommended_reviews(request: Request, db: Session = Depends(get_db)):
    """
    Genera las recomendaciones de álbumes cruzando los datos de Pitchfork y Spotify.
    """
    spotify_user_id = request.cookies.get("spotify_user_id")
    if not spotify_user_id:
        raise HTTPException(status_code=400, detail="Spotify user ID missing in cookies")

    # Obtener nuestro user_id de base de datos
    user = db.query(user_service.User).filter_by(spotify_user_id=spotify_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reviews = get_recommended_reviews(user.id, db)
    return reviews
