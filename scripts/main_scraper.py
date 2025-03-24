import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.pitchfork_scraper import get_album_urls, get_review_details
from app.utils.csv_utils import save_reviews_to_csv
from app.core.database import SessionLocal
from app.services.pitchfork_service import save_reviews_to_db
from app.utils.logger import logger


def main():
    urls = get_album_urls()
    reviews = []
    for url in urls:
        review = get_review_details(url)
        if review:
            reviews.append(review)

    save_reviews_to_csv(reviews)
    logger.info(f"{len(reviews)} reseñas insertadas en la BBDD.")

    db = SessionLocal()
    save_reviews_to_db(db, reviews)
    db.close()

if __name__ == "__main__":
    main()
