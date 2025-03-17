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

if not API_KEY:
    raise ValueError("No se ha encontrado una API Key de ScrapingBee en el archivo .env")

# Crear cliente de ScrapingBee
client = ScrapingBeeClient(api_key=API_KEY)

# Función para obtener los enlaces de los álbumes y navegar por las páginas
def get_album_urls():
    album_urls = []
    page = 1  # Comenzamos con la primera página
    
    while page <= 2:  # Limitar a las primeras 2 páginas para pruebas
        url = f"{BASE_URL}?page={page}"
        
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
            album_urls.append(link.get('href'))

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
    scrapingbee_url = f'https://app.scrapingbee.com/api/v1/?api_key={API_KEY}&url={album_url}'

    try:
        response = requests.get(scrapingbee_url)
        response.raise_for_status()  # Esto lanzará una excepción si el código de estado no es 2xx
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud de detalles del álbum: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        title = soup.find('h1', class_='SplitScreenContentHeaderHed-lcUSuI').get_text(strip=True)
    except AttributeError:
        title = "Desconocido"

    try:
        artist = soup.find('a', class_='SplitScreenContentHeaderArtistLink-joHTqI').get_text(strip=True)
    except AttributeError:
        artist = "Desconocido"
        
    try:
        release_year = soup.find('time', class_='SplitScreenContentHeaderReleaseYear-UjuHP').get_text(strip=True)
    except AttributeError:
        release_year = "Desconocido"
        
    try:
        rating = soup.find('p', class_='Rating-bkjebD').get_text(strip=True)
    except AttributeError:
        rating = "Desconocido"
   
    # Extraer género y sello (label)
    genre = None
    label = None
    
    # Buscar dentro del <ul> con la clase 'InfoSliceList-daJBOF'
    info_list = soup.find('ul', class_='InfoSliceList-daJBOF bZHSGv')
    
    if info_list:
        for li in info_list.find_all('li', class_='InfoSliceListItem-hNmIoI'):
            key = li.find('p', class_='BaseWrap-sc-gjQpdd BaseText-ewhhUZ InfoSliceKey-gHIvng').get_text(strip=True)
            value = li.find('p', class_='BaseWrap-sc-gjQpdd BaseText-ewhhUZ InfoSliceValue-tfmqg').get_text(strip=True)
            
            if "Genre" in key:
                genre = value
            elif "Label" in key:
                label = value
    
    try:
        reviewer = soup.find('span', class_='BylineName-kwmrLn').get_text(strip=True)
    except AttributeError:
        reviewer = "Desconocido"

    try:
        review_text = soup.find('div', class_='SplitScreenContentHeaderDekDown-csTFQR').get_text(strip=True)
    except AttributeError:
        review_text = "No disponible"

    album = Album(title, artist, release_year, rating, genre, label, reviewer, review_text, album_url)
    return album

# Función para guardar los datos en un archivo CSV
def save_albums_to_csv(albums):
    if not os.path.exists('data'):
        os.makedirs('data')

    with open('data/albums.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Artist', 'Release Year', 'Rating', 'Genre', 'Label', 'Reviewer', 'Review Text', 'URL'])

        for album in albums:
            writer.writerow([album.title, album.artist, album.release_year, album.rating, album.genre, album.label, album.reviewer, album.review_text, album.album_url])
