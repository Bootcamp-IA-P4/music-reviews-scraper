from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class SavedAlbum(Base):
    __tablename__ = "spotify_saved_albums"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    artist = Column(String)
    label = Column(String)
    release_year = Column(String)
    url = Column(String)
