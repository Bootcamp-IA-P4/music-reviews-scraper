from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class SavedAlbum(Base):
    __tablename__ = "spotify_saved_albums"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    label = Column(String)
    release_date = Column(Date)
    url = Column(String)


