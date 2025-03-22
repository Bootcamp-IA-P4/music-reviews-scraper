from sqlalchemy import Column, String, DateTime
from app.core.database import Base
from datetime import datetime

class SpotifyToken(Base):
    __tablename__ = 'spotify_tokens'
    user_id = Column(String, primary_key=True, index=True)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)  
