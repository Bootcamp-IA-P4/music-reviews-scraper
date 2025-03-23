from sqlalchemy.orm import Session
from app.models.spotify import SavedAlbum
from app.models.pitchfork import AlbumReview
from sqlalchemy import or_

def get_recommended_reviews(user_id: str, db: Session):
    saved_albums = db.query(SavedAlbum).filter_by(user_id=user_id).all()
    recommended = {}
    
    for album in saved_albums:
        spotify_artists = [artist.strip().lower() for artist in album.artist.split(",")]
        spotify_title = album.title.strip().lower()

        artist_conditions = [
            AlbumReview.artist.ilike(f"%{artist}%") for artist in spotify_artists
        ]

        query = db.query(AlbumReview).filter(
            or_(
                *artist_conditions,
                AlbumReview.title.ilike(f"%{spotify_title}%")
            )
        )

        matches = query.all()
        for match in matches:
            # Usamos la URL de Pitchfork como clave para evitar duplicados
            if match.url not in recommended:
                recommended[match.url] = {
                    "id": match.id,
                    "title": match.title,
                    "artist": match.artist,
                    "rating": match.rating,
                    "reviewer": match.reviewer,
                    "label": match.label,
                    "url": match.url
                }

    # Devolvemos solo los valores únicos
    return list(recommended.values())
