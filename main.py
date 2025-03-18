from scraping.pitchfork_scraper import get_album_urls, get_review_details, save_albums_to_csv

def main():
    album_urls = get_album_urls()
    albums = []

    for album_url in album_urls:
        album = get_review_details(album_url)
        if album:
            albums.append(album)

    save_albums_to_csv(albums)
    print(f"Se han guardado {len(albums)} álbumes en el archivo CSV.")

if __name__ == '__main__':
    main()
