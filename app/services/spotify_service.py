from app.models.spotify import SavedAlbum
from app.core.database import get_db
from sqlalchemy.orm import Session

def save_spotify_albums(user_id: str, albums_list: list, db: Session):
    db.query(SavedAlbum).filter_by(user_id=user_id).delete()

    for album in albums_list:
        existing_album = db.query(SavedAlbum).filter_by(
            user_id=user_id,
            title=album['title'],
            artist=', '.join(album['artists']) 
        ).first()
        if not existing_album:
            saved_album = SavedAlbum(
                user_id=user_id,
                title=album['title'],
                artist=', '.join(album['artists']),
                label=album.get('label'),
                release_year=album.get('release_year'),
                url=album.get('url')
            )
            db.add(saved_album)
    db.commit()
