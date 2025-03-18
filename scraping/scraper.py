import requests
import os
import csv
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from scraping.album import Album
from scrapingbee import ScrapingBeeClient

load_dotenv()

API_KEY = os.getenv('SCRAPINGBEE_API_KEY')
BASE_URL = os.getenv('BASE_URL')
ALBUM_REVIEWS_URL = os.getenv('ALBUM_REVIEWS_URL')

if not API_KEY:
    raise ValueError("No se ha encontrado una API Key de ScrapingBee en el archivo .env")

client = ScrapingBeeClient(api_key=API_KEY)

# Obtener los enlaces de los álbumes
def get_album_urls():
    album_urls = []
    page = 1

    while page <= 2:
        url = f"{ALBUM_REVIEWS_URL}?page={page}"
        try:
            response = client.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error al hacer la solicitud a la página {page}: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        album_links = soup.find_all('a', class_='SummaryItemHedLink-civMjp')

        if not album_links:
            print("No se encontraron más álbumes. Terminando.")
            break

        for link in album_links[:2]:  # Limita a 2 álbumes por página en pruebas
            href = link.get('href')
            if href.startswith('/'):
                href = href.lstrip('/')
            album_urls.append(href)

        # Verificar si hay siguiente página
        next_page = soup.find('a', class_='BaseButton-bLlsy', string='Next Page')
        if not next_page:
            print("No hay más páginas. Terminando.")
            break

        page += 1
        time.sleep(2)

    return album_urls

# Extraer detalles de un álbum
def get_album_details(album_url):
    url = f"{BASE_URL.rstrip('/')}/{album_url.lstrip('/')}"
    try:
        response = client.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud de detalles del álbum: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # ✅ Captura más robusta del título
    title_tag = soup.find('h1', {'data-testid': 'ContentHeaderHed'})
    title = title_tag.get_text(strip=True) if title_tag else "Desconocido"

    # ✅ Captura múltiple de artistas
    artist_tags = soup.select('ul.SplitScreenContentHeaderArtistWrapper-fiSZLT a')
    artist = ", ".join([a.get_text(strip=True) for a in artist_tags]) if artist_tags else "Desconocido"

    # ✅ Año de lanzamiento
    release_tag = soup.find('time', {'data-testid': 'SplitScreenContentHeaderReleaseYear'})
    release_year = release_tag.get_text(strip=True) if release_tag else "Desconocido"

    # ✅ Rating
    rating = "Desconocido"
    score_box = soup.find('div', class_='ScoreBoxWrapper-iBCGEf')
    if score_box:
        rating_tag = score_box.find('p', class_=lambda x: x and 'Rating-' in x)
        rating = rating_tag.get_text(strip=True) if rating_tag else "Desconocido"


    # ✅ Inicializar género y label por cada álbum con diccionario
    genre, label = "Desconocido", "Desconocido"
    info_dict = {}
    for li in soup.select('li.InfoSliceListItem-hNmIoI'):
        key_tag = li.select_one('p.InfoSliceKey-gHIvng')
        value_tag = li.select_one('p.InfoSliceValue-tfmqg')
        if key_tag and value_tag:
            key_text = key_tag.get_text(strip=True).replace(":", "")
            value_text = value_tag.get_text(strip=True)
            info_dict[key_text] = value_text

    genre = info_dict.get("Genre", "Desconocido")
    label = info_dict.get("Label", "Desconocido")

    # ✅ Nombre del reviewer
    reviewer_tag = soup.find('span', class_='BylineName-kwmrLn')
    reviewer = reviewer_tag.get_text(strip=True) if reviewer_tag else "Desconocido"

    # ✅ Texto de la review (Dek)
    review_text_tag = soup.find('div', class_='SplitScreenContentHeaderDekDown-csTFQR')
    review_text = review_text_tag.get_text(strip=True) if review_text_tag else "No disponible"

    return Album(title, artist, release_year, rating, genre, label, reviewer, review_text, url)

# Guardar los datos en CSV
def save_albums_to_csv(albums):
    if not os.path.exists('data'):
        os.makedirs('data')

    with open('data/albums.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Artist', 'Release Year', 'Rating', 'Genre', 'Label', 'Reviewer', 'Review Text', 'URL'])

        for album in albums:
            writer.writerow([album.title, album.artist, album.release_year, album.rating, album.genre, album.label, album.reviewer, album.review_text, album.url])
