from app.core.database import SessionLocal
from app.models.pitchfork import AlbumReview
from app.models.spotify import SavedAlbum

def check_tables():
    db = SessionLocal()
    reviews_count = db.query(AlbumReview).count()
    saved_albums_count = db.query(SavedAlbum).count()
    print(f"Total de reviews de pitchfork en la BBDD: {reviews_count}")
    print(f"Total de álbumes de spotify en la BBDD: {saved_albums_count}")
    db.close()


if __name__ == "__main__":
    check_tables()