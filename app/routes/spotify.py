from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from datetime import datetime
from typing import Dict, Optional
import os
import urllib.parse

# Configuración y servicios
from app.core.config import settings
from app.services.spotify_service import save_spotify_albums
from app.core.database import SessionLocal

CLIENT_ID = settings.SPOTIFY_CLIENT_ID
CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET
REDIRECT_URI = settings.SPOTIFY_REDIRECT_URI

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"

SCOPES = ["user-read-email", "user-read-private", "playlist-read-private", "user-library-read"]

router = APIRouter()

# Simulando sesión temporal (idealmente usar Redis o persistencia real)
session: Dict[str, Optional[str]] = {}

@router.get("/login")
async def login():
    params = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "client_id": CLIENT_ID,
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(auth_url)

@router.get("/callback")
async def callback(code: str, error: Optional[str] = None):
    if error:
        raise HTTPException(status_code=400, detail=f"Error: {error}")

    async with httpx.AsyncClient() as client:
        req_body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        response = await client.post(TOKEN_URL, data=req_body)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to exchange code for token")

        token_info = response.json()

    # Guardamos tokens en la "sesión"
    session['access_token'] = token_info.get('access_token')
    session['refresh_token'] = token_info.get('refresh_token')
    session['expires_at'] = datetime.now().timestamp() + token_info.get('expires_in', 3600)

    return RedirectResponse("/saved_albums")

async def refresh_access_token():
    if 'refresh_token' not in session:
        raise HTTPException(status_code=401, detail="User not logged in or refresh token missing")

    async with httpx.AsyncClient() as client:
        req_body = {
            "grant_type": "refresh_token",
            "refresh_token": session['refresh_token'],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        response = await client.post(TOKEN_URL, data=req_body)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to refresh token")

        new_token_info = response.json()

    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + new_token_info.get('expires_in', 3600)

async def check_and_refresh_token():
    if 'access_token' not in session:
        raise HTTPException(status_code=401, detail="User not logged in")

    if datetime.now().timestamp() > session['expires_at']:
        await refresh_access_token()

@router.get("/saved_albums")
async def saved_albums():
    await check_and_refresh_token()
    headers = {'Authorization': f"Bearer {session['access_token']}"}

    albums_list = []
    limit = 50
    offset = 0
    max_albums = 500

    async with httpx.AsyncClient() as client:
        while len(albums_list) < max_albums:
            response = await client.get(
                f"{API_BASE_URL}/me/albums?limit={limit}&offset={offset}",
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

    # Guardar en la base de datos
    db = SessionLocal()
    try:
        save_spotify_albums(user_id="test_user", albums_list=albums_list, db=db)
    finally:
        db.close()

    return {"saved_albums": albums_list}
