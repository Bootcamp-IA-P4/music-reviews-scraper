from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.recommended_service import get_recommended_reviews
from app.services import user_service

router = APIRouter()

@router.get("/recommended_reviews")
def recommended_reviews(
    spotify_user_id: str = Query(None),
    artist: str = Query(None),
    db: Session = Depends(get_db)
):    
    """
    Genera las recomendaciones de álbumes cruzando los datos de Pitchfork y Spotify.
    """

    if not spotify_user_id:
        raise HTTPException(status_code=400, detail="Spotify user ID missing (param or cookie)")

    # Buscar al usuario en la base de datos
    user = db.query(user_service.User).filter_by(spotify_user_id=spotify_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reviews = get_recommended_reviews(user.id, db)
    
    if artist:
        filtered_reviews = []
        for review in reviews:
            if review.get('artist') is not None and artist.lower() in review['artist'].lower():
                filtered_reviews.append(review)
        reviews = filtered_reviews

    return reviews
