from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
from app.services import spotify_service, user_service

client = TestClient(app)

# Test para /reviews
def test_get_reviews():
    response = client.get("/reviews")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "title" in data[0]
        assert "artist" in data[0]
        assert "rating" in data[0]
        assert "label" in data[0]

# Test para /saved_albums con usuario válido
def test_get_saved_albums():
    spotify_user_id = "aalonsoco"  
    mock_user = MagicMock()
    mock_user.id = 1 
    with patch.object(user_service, "get_or_create_user", return_value=mock_user):
        with patch.object(spotify_service, "fetch_and_store_saved_albums", return_value=[
            {
                "title": "Highway 61 Revisited",
                "artists": ["Bob Dylan"],
                "label": "Columbia",
                "release_year": "1965",
                "url": "https://open.spotify.com/album/6YabPKtZAjxwyWbuO9p4ZD"
            }
        ]) as mock_fetch:
            response = client.get(f"/saved_albums?spotify_user_id={spotify_user_id}")
            assert response.status_code == 200
            data = response.json()
            assert "saved_albums" in data
            assert isinstance(data["saved_albums"], list)
            assert "title" in data["saved_albums"][0]
            mock_fetch.assert_called_once() 

# Test para /saved_albums con usuario inexistente
def test_get_saved_albums_user_not_found():
    spotify_user_id = "unknown_user"
    with patch.object(user_service, "get_or_create_user", return_value=None):
        response = client.get(f"/saved_albums?spotify_user_id={spotify_user_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

# Test para /login
def test_login_redirect():
    response = client.get("/login", follow_redirects=False)
    assert response.status_code == 307 
    assert "https://accounts.spotify.com/authorize" in response.headers["location"]

# Test para /callback con error
def test_callback_error():
    # Enviamos un code inválido junto al error para evitar el 422 de FastAPI
    response = client.get("/callback?code=invalid_code&error=access_denied")
    assert response.status_code == 400
    # Ajustamos la aserción al mensaje real que devuelve la API
    assert response.json()["detail"] == "Error: access_denied"
