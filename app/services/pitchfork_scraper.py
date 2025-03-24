import requests
import os
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

API_KEY = os.getenv('SCRAPER_API_KEY')
BASE_URL = os.getenv('BASE_URL')
ALBUM_REVIEWS_URL = os.getenv('ALBUM_REVIEWS_URL')
SCRAPERAPI_URL = 'https://api.scraperapi.com/'

if not API_KEY:
    logger.error("No se ha encontrado una API Key de ScraperAPI en el archivo .env")
    raise ValueError("No se ha encontrado una API Key de ScraperAPI en el archivo .env")

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

def scraperapi_get(target_url):
    logger.debug(f"Lanzando request a ScraperAPI para la URL: {target_url}")
    payload = {'api_key': API_KEY, 'url': target_url}
    response = requests.get(SCRAPERAPI_URL, params=payload)
    logger.debug(f"Respuesta recibida de ScraperAPI: {response.status_code}")
    return response

def get_album_urls():
    album_urls = []
    page = 1

    while page <= 1:  # Limitar a 1 página para pruebas
        url = f"{ALBUM_REVIEWS_URL}?page={page}"
        logger.info(f"Scrapeando página de reviews: {url}")
        try:
            response = scraperapi_get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en la solicitud de la página {page}: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        album_links = soup.find_all('a', class_='SummaryItemHedLink-civMjp')

        if not album_links:
            logger.warning("No se encontraron más álbumes en esta página. Terminando.")
            break

        for link in album_links[:10]:  # Limitar para pruebas
            href = link.get('href')
            if href.startswith('/'):
                href = href.lstrip('/')
            album_urls.append(href)
            logger.debug(f"Álbum encontrado: {href}")

        next_page = soup.find('a', class_='BaseButton-bLlsy', string='Next Page')
        if not next_page:
            logger.info("No hay más páginas. Scraping terminado.")
            break

        page += 1

    logger.info(f"Total de álbumes encontrados: {len(album_urls)}")
    return album_urls

def get_review_details(album_url):
    url = f"{BASE_URL.rstrip('/')}/{album_url.lstrip('/')}"
    logger.info(f"Scrapeando detalles del álbum: {url}")
    try:
        response = scraperapi_get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error en la solicitud de detalles del álbum: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    try:
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
        
        # Género y sello discográfico
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

        logger.info(f"Review extraída correctamente: {title} - {artist}")
        return Review(title, artist, release_year, rating, genre, label, reviewer, review_text, url)

    except Exception as e:
        logger.exception(f"Error al parsear los detalles del álbum: {e}")
        return None
