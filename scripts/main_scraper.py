import sys
import os

# Agregar la ruta de la raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraping.pitchfork_scraper import get_album_urls, get_review_details,  save_reviews_to_csv
from database.database import SessionLocal
from database.crud import save_reviews_to_db

def main():
    urls = get_album_urls()
    reviews = []
    for url in urls:
        review = get_review_details(url)
        if review:
            reviews.append(review)

    save_reviews_to_csv(reviews)
    print(f"Se han guardado {len(reviews)} álbumes en el archivo CSV.")

    db = SessionLocal()
    save_reviews_to_db(db, reviews)
    db.close()

if __name__ == "__main__":
    main()
