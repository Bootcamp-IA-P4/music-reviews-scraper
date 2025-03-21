from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.core.database import Base

class SavedAlbum(Base):
    __tablename__ = "spotify_saved_albums"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    album_name = Column(String, nullable=False)
    artist_name = Column(String, nullable=False)
    label = Column(String)
    release_date = Column(Date)
    external_url = Column(String)
