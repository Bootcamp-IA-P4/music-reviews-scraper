from sqlalchemy.orm import Session
from app.models.spotify import SavedAlbum
from app.models.pitchfork import AlbumReview

def get_recommended_reviews(user_id: str, db: Session):
    saved_albums = db.query(SavedAlbum).filter_by(user_id=user_id).all()
    recommended = []

    for album in saved_albums:
        query = db.query(AlbumReview).filter(
            (AlbumReview.artist.ilike(f"%{album.artist}%")) |
            (AlbumReview.title.ilike(f"%{album.title}%")) |
            (AlbumReview.label.ilike(f"%{album.label}%"))
        )
        matches = query.all()
        for match in matches:
            recommended.append({
                "pitchfork_title": match.title,
                "pitchfork_artist": match.artist,
                "rating": match.rating,
                "label": match.label,
                "spotify_album": album.title,
                "spotify_artist": album.artist
            })

    return recommended
