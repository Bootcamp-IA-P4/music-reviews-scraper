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

# Crear cliente de ScrapingBee
client = ScrapingBeeClient(api_key=API_KEY)

# Función para obtener los enlaces de los álbumes y navegar por las páginas
def get_album_urls():
    album_urls = []
    page = 1  # Comenzamos con la primera página
    
    while page <= 2:  # Limitar a las primeras 2 páginas para pruebas
        url = f"{ALBUM_REVIEWS_URL}?page={page}"
        
         # Usamos el cliente de ScrapingBee para obtener el HTML de la página
        try:
            response = client.get(url)
            response.raise_for_status()  # Esto lanzará una excepción si el código de estado no es 2xx
        except requests.exceptions.RequestException as e:
            print(f"Error al hacer la solicitud a la página {page}: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        
        album_links = soup.find_all('a', class_='SummaryItemHedLink-civMjp')
        
        if not album_links:
            print("No se encontraron más álbumes. Terminando.")
            break

        for link in album_links[:2]:  #  Limitar los álbumes a solo 2 para pruebas
            href = link.get('href')
            if href.startswith('/'):
                href = href.lstrip('/')  # Elimina la barra inicial para evitar doble slash en la concatenación
            album_urls.append(href)

        next_page = soup.find('a', class_='BaseButton-bLlsy')
        
        if not next_page:
            print("No hay más páginas. Terminando.")
            break

        page += 1

        # Esperar entre 1 y 3 segundos entre solicitudes para no sobrecargar el servidor
        time.sleep(2)

    return album_urls

# Función para extraer los detalles de un álbum
def get_album_details(album_url):
    url = f"{BASE_URL.rstrip('/')}/{album_url.lstrip('/')}" 

    try:
        response = client.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud de detalles del álbum: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1', class_='SplitScreenContentHeaderHed-lcUSuI')
    title = title.get_text(strip=True) if title else "Desconocido"

    artist = soup.find('a', class_='SplitScreenContentHeaderArtistLink-joHTqI')
    artist = artist.get_text(strip=True) if artist else "Desconocido"

    release_year = soup.find('time', class_='SplitScreenContentHeaderReleaseYear-UjuHP')
    release_year = release_year.get_text(strip=True) if release_year else "Desconocido"

    rating = soup.find('p', class_='Rating-bkjebD')
    rating = rating.get_text(strip=True) if rating else "Desconocido"

    # Extraer género y sello discográfico
    genre, label = "Desconocido", "Desconocido"
    info_list = soup.find('ul', class_='InfoSliceList-daJBOF bZHSGv')

    if info_list:
        for li in info_list.find_all('li', class_='InfoSliceListItem-hNmIoI'):
            key = li.find('p', class_='BaseWrap-sc-gjQpdd BaseText-ewhhUZ InfoSliceKey-gHIvng')
            value = li.find('p', class_='BaseWrap-sc-gjQpdd BaseText-ewhhUZ InfoSliceValue-tfmqg')

            key_text = key.get_text(strip=True) if key else ""
            value_text = value.get_text(strip=True) if value else ""

            if "Genre" in key_text:
                genre = value_text
            elif "Label" in key_text:
                label = value_text

    reviewer = soup.find('span', class_='BylineName-kwmrLn')
    reviewer = reviewer.get_text(strip=True) if reviewer else "Desconocido"

    review_text = soup.find('div', class_='SplitScreenContentHeaderDekDown-csTFQR')
    review_text = review_text.get_text(strip=True) if review_text else "No disponible"

    return Album(title, artist, release_year, rating, genre, label, reviewer, review_text, url)

# Función para guardar los datos en un archivo CSV
def save_albums_to_csv(albums):
    if not os.path.exists('data'):
        os.makedirs('data')

    with open('data/albums.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Artist', 'Release Year', 'Rating', 'Genre', 'Label', 'Reviewer', 'Review Text', 'URL'])

        for album in albums:
            writer.writerow([album.title, album.artist, album.release_year, album.rating, album.genre, album.label, album.reviewer, album.review_text, album.url])
