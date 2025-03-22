from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    spotify_user_id = Column(String, unique=True, index=True)
    email = Column(String)

    spotify_tokens = relationship("SpotifyToken", back_populates="user")
