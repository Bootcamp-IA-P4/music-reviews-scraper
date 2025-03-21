import requests
import os
import csv
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('SCRAPER_API_KEY')
BASE_URL = os.getenv('BASE_URL')
ALBUM_REVIEWS_URL = os.getenv('ALBUM_REVIEWS_URL')

if not API_KEY:
    raise ValueError("No se ha encontrado una API Key de ScraperAPI en el archivo .env")

SCRAPERAPI_URL = 'https://api.scraperapi.com/'


class Review:
    def __init__(self, title, artist, release_year, rating, genre, label, reviewer, review_text, url):
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.rating = rating
        self.genre = genre
        self.label = label
        self.reviewer = reviewer
        self.review_text = review_text
        self.url = url

# Función para hacer requests a través de ScraperAPI
def scraperapi_get(target_url):
    payload = {
        'api_key': API_KEY,
        'url': target_url
    }
    response = requests.get(SCRAPERAPI_URL, params=payload)
    return response

# Obtener los enlaces de los álbumes
def get_album_urls():
    album_urls = []
    page = 1

    while page <= 40:  # Límite de 40 páginas para no exceder el límite de requests gratuitas de ScraperAPI
        url = f"{ALBUM_REVIEWS_URL}?page={page}"
        try:
            response = scraperapi_get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error al hacer la solicitud a la página {page}: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        album_links = soup.find_all('a', class_='SummaryItemHedLink-civMjp')

        if not album_links:
            print("No se encontraron más álbumes. Terminando.")
            break

        for link in album_links:
            href = link.get('href')
            if href.startswith('/'):
                href = href.lstrip('/')
            album_urls.append(href)

        next_page = soup.find('a', class_='BaseButton-bLlsy', string='Next Page')
        if not next_page:
            print("No hay más páginas. Terminando.")
            break

        page += 1
        time.sleep(1)

    return album_urls

# Extraer detalles de un álbum
def get_review_details(album_url):
    url = f"{BASE_URL.rstrip('/')}/{album_url.lstrip('/')}"
    try:
        response = scraperapi_get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud de detalles del álbum: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Título
    title_tag = soup.find('h1', {'data-testid': 'ContentHeaderHed'})
    title = title_tag.get_text(strip=True) if title_tag else None

    # Artistas
    artist_tags = soup.select('ul.SplitScreenContentHeaderArtistWrapper-fiSZLT a')
    artist = ", ".join([a.get_text(strip=True) for a in artist_tags]) if artist_tags else None

    # Año de lanzamiento
    release_tag = soup.find('time', {'data-testid': 'SplitScreenContentHeaderReleaseYear'})
    release_year = release_tag.get_text(strip=True) if release_tag else None

    # Rating
    rating = None
    score_box = soup.find('div', class_='ScoreBoxWrapper-iBCGEf')
    if score_box:
        rating_tag = score_box.find('p', class_=lambda x: x and 'Rating-' in x)
        rating = rating_tag.get_text(strip=True) if rating_tag else None

    # Género y sello
    genre, label = None, None
    info_dict = {}
    for li in soup.select('li.InfoSliceListItem-hNmIoI'):
        key_tag = li.select_one('p.InfoSliceKey-gHIvng')
        value_tag = li.select_one('p.InfoSliceValue-tfmqg')
        if key_tag and value_tag:
            key_text = key_tag.get_text(strip=True).replace(":", "")
            value_text = value_tag.get_text(strip=True)
            info_dict[key_text] = value_text

    genre = info_dict.get("Genre")
    label = info_dict.get("Label")

    # Reviewer
    reviewer_tag = soup.find('span', class_='BylineName-kwmrLn')
    reviewer_link = reviewer_tag.find('a') if reviewer_tag else None
    reviewer = reviewer_link.get_text(strip=True) if reviewer_link else None

    # Texto de la review
    review_text_tag = soup.find('div', class_='SplitScreenContentHeaderDekDown-csTFQR')
    review_text = review_text_tag.get_text(strip=True) if review_text_tag else None

    return Review(title, artist, release_year, rating, genre, label, reviewer, review_text, url)
