import httpx
from app.core.database import SessionLocal
from app.services import spotify_token_service
from app.models.spotify import SavedAlbum
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.config import settings

SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

def save_spotify_albums(user_id: str, albums_list: list, db: Session):
    """
    Guarda la lista de álbumes en la base de datos.
    """
    db.query(SavedAlbum).filter_by(user_id=user_id).delete()
    for album in albums_list:
        existing_album = db.query(SavedAlbum).filter_by(
            user_id=user_id,
            title=album['title'],
            artist=', '.join(album['artists']) 
        ).first()
        if not existing_album:
            saved_album = SavedAlbum(
                user_id=user_id,
                title=album['title'],
                artist=', '.join(album['artists']),
                label=album.get('label'),
                release_year=album.get('release_year'),
                url=album.get('url')
            )
            db.add(saved_album)
    db.commit()

async def fetch_and_store_saved_albums(user_id: str):
    """
    Obtiene los saved albums de Spotify y los almacena en la base de datos.
    """
    access_token = await spotify_token_service.check_and_refresh_token(user_id)
    headers = {'Authorization': f"Bearer {access_token}"}
    albums_list = []
    limit = 50
    offset = 0
    max_albums = 200  # Límite de álbumes a obtener

    async with httpx.AsyncClient() as client:
        while len(albums_list) < max_albums:
            response = await client.get(
                f"{SPOTIFY_API_BASE_URL}/me/albums?limit={limit}&offset={offset}",
                headers=headers
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch saved albums")

            albums_data = response.json()
            items = albums_data.get('items', [])
            if not items:
                break  # No hay más álbumes

            for item in items:
                album = item.get('album', {})
                album_info = {
                    'title': album.get('name'),
                    'artists': [artist['name'] for artist in album.get('artists', [])],
                    'label': album.get('label'),
                    'release_year': album.get('release_date', '').split("-")[0],
                    'url': album.get('external_urls', {}).get('spotify'),
                }
                albums_list.append(album_info)
            offset += limit

    db = SessionLocal()
    try:
        save_spotify_albums(user_id, albums_list, db)
    finally:
        db.close()

    return albums_list
