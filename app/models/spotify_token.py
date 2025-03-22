from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class SpotifyToken(Base):
    __tablename__ = 'spotify_tokens'
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)  

    user = relationship("User", back_populates="spotify_tokens")
