from scraping.scraper import get_album_urls, get_album_details, save_albums_to_csv

def main():
    album_urls = get_album_urls()  # Obtener los enlaces de los álbumes (solo 2 páginas)
    albums = []

    for album_url in album_urls:
        album = get_album_details(album_url)  # Obtener detalles de cada álbum
        if album:
            albums.append(album)

    save_albums_to_csv(albums)  # Guardar en CSV
    print(f"Se han guardado {len(albums)} álbumes en el archivo CSV.")

if __name__ == '__main__':
    main()
