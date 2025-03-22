from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from app.services import spotify_token_service, spotify_service
from app.core.config import settings

import urllib.parse

router = APIRouter()

SPOTIFY_SCOPES = [
    "user-read-email", "user-read-private",
    "playlist-read-private", "user-library-read"
]

@router.get("/login")
async def login():
    """
    Redirige al usuario a la autorización de Spotify
    """
    params = {
        "response_type": "code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "scope": " ".join(SPOTIFY_SCOPES),
        "client_id": settings.SPOTIFY_CLIENT_ID,
    }
    auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"
    return RedirectResponse(auth_url)

@router.get("/callback")
async def callback(code: str, error: str = None):
    """
    Callback tras la autenticación de Spotify.
    Guarda los tokens en la base de datos.
    """
    if error:
        raise HTTPException(status_code=400, detail=f"Error: {error}")

    token_info = await spotify_token_service.exchange_code_for_token(code)
    user_id = "test_user"  # Cambiar luego por usuario real
    await spotify_token_service.store_token(user_id, token_info)

    return RedirectResponse("/saved_albums")

@router.get("/saved_albums")
async def saved_albums():
    """
    Obtiene los álbumes guardados del usuario y los almacena en la base de datos
    """
    user_id = "test_user"  # Luego se obtiene de la autenticación real
    albums_list = await spotify_service.fetch_and_store_saved_albums(user_id)
    return {"saved_albums": albums_list}
