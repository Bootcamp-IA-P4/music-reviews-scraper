from sqlalchemy.orm import Session
from app.models.user import User

def get_or_create_user(db: Session, spotify_user_id: str, email: str = None):
    user = db.query(User).filter_by(spotify_user_id=spotify_user_id).first()
    if not user:
        user = User(spotify_user_id=spotify_user_id, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user