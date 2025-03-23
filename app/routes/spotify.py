from fastapi import APIRouter, HTTPException, Depends, Response, Request, Query
from fastapi.responses import RedirectResponse, JSONResponse
from app.services import spotify_token_service, spotify_service, user_service
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
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
        "show_dialog": True
    }
    auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"
    return RedirectResponse(auth_url)

@router.get("/callback")
async def callback(code: str, error: str = None, db: Session = Depends(get_db)):
    """
    Callback tras la autenticación de Spotify.
    Guarda los tokens en la base de datos y registra/recupera el usuario real.
    """
    if error:
        raise HTTPException(status_code=400, detail=f"Error: {error}")

    # Intercambiamos el código por el token
    token_info = await spotify_token_service.exchange_code_for_token(code)

    # Obtenemos el perfil de Spotify con el access_token
    profile = await spotify_service.get_user_profile(token_info["access_token"])
    spotify_user_id = profile["id"]
    email = profile.get("email")

    # Guardamos o recuperamos el usuario en nuestra base de datos
    user = user_service.get_or_create_user(db, spotify_user_id, email)

    # Guardamos el token usando el user.id de nuestra base de datos
    await spotify_token_service.store_token(user.id, token_info)

    try:
        albums_list = await spotify_service.fetch_and_store_saved_albums(user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al almacenar los álbumes: {str(e)}")


    # Redirigimos a la vista del frontend y seteamos una cookie con el spotify_user_id para el backend
    frontend_url = f"http://localhost:3000/recommended?spotify_user_id={spotify_user_id}"
    response = RedirectResponse(url=frontend_url)
    return response


@router.get("/saved_albums")
async def saved_albums(
    spotify_user_id: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    Obtiene los álbumes guardados del usuario de Spotify y los almacena en la base de datos.
    Se prioriza el spotify_user_id recibido por query param, pero si no se recibe, 
    se intenta recuperar de las cookies.
    """

    if not spotify_user_id:
        raise HTTPException(status_code=400, detail="Spotify user ID missing (param or cookie)")

    # Buscamos al usuario en nuestra base de datos usando el spotify_user_id
    user = db.query(user_service.User).filter_by(spotify_user_id=spotify_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Ahora usamos el user.id de nuestra base de datos
    albums_list = await spotify_service.fetch_and_store_saved_albums(user.id)

    # Opcional: redirigir directamente a las recomendaciones
    # return RedirectResponse(url="/recommended_reviews")

    # O devolver los albums y que el front decida
    return {"saved_albums": albums_list}