import httpx
from app.models.spotify_token import SpotifyToken
from app.core.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.config import settings
from datetime import datetime, timezone, timedelta

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

def save_or_update_token(db: Session, user_id: str, access_token: str, refresh_token: str, expires_in: int):
    """
    Guarda o actualiza el token en la base de datos.
    """
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    token = db.query(SpotifyToken).filter_by(user_id=user_id).first()
    if token:
        token.access_token = access_token
        token.refresh_token = refresh_token
        token.expires_at = expires_at
    else:
        token = SpotifyToken(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at
        )
        db.add(token)
    db.commit()

def get_token(db: Session, user_id: str):
    """
    Recupera el token de la base de datos.
    """
    return db.query(SpotifyToken).filter_by(user_id=user_id).first()

async def exchange_code_for_token(code: str):
    """
    Intercambia el código de autorización por un token de acceso y refresh.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(SPOTIFY_TOKEN_URL, data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "client_secret": settings.SPOTIFY_CLIENT_SECRET
        })
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to exchange code for token")
        return response.json()

async def store_token(user_id: str, token_info: dict):
    """
    Almacena el token en la base de datos.
    """
    db = SessionLocal()
    try:
        save_or_update_token(
            db,
            user_id,
            token_info.get('access_token'),
            token_info.get('refresh_token'),
            token_info.get('expires_in', 3600)
        )
    finally:
        db.close()

async def check_and_refresh_token(user_id: str) -> str:
    """
    Verifica la validez del token y lo refresca si es necesario.
    """
    db = SessionLocal()
    token_data = get_token(db, user_id)
    if not token_data:
        db.close()
        raise HTTPException(status_code=401, detail="No token found for user")

    if token_data.expires_at.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):        
        print("🔄 Token expirado. Refrescando...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                SPOTIFY_TOKEN_URL,
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': token_data.refresh_token,
                    'client_id': settings.SPOTIFY_CLIENT_ID,
                    'client_secret': settings.SPOTIFY_CLIENT_SECRET
                }
            )
            if response.status_code != 200:
                db.close()
                raise HTTPException(status_code=400, detail="Failed to refresh token")

            refreshed = response.json()
            access_token = refreshed['access_token']
            expires_in = refreshed.get('expires_in', 3600)
            save_or_update_token(db, user_id, access_token, token_data.refresh_token, expires_in)
    else:
        access_token = token_data.access_token

    db.close()
    return access_token
