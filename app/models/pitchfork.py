from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from app.core.database import Base

class AlbumReview(Base):
    __tablename__ = 'pitchfork_reviews'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    artist = Column(String, nullable=True)
    release_year = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    genre = Column(String, nullable=True)
    label = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    review_text = Column(String, nullable=True)
    url = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('title', 'artist', name='uix_title_artist'),)
