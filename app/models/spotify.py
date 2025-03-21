from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class SavedAlbum(Base):
    __tablename__ = "spotify_saved_albums"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    title = Column(String)
    artist = Column(String)
    label = Column(String)
    release_year = Column(String)
    url = Column(String)


