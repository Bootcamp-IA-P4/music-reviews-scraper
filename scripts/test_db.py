from app.core.database import SessionLocal
from app.models.pitchfork import AlbumReview
from app.models.spotify import SavedAlbum

db = SessionLocal()
print(db.query(AlbumReview).count())
print(db.query(SavedAlbum).count())
db.close()
