from database.models import AlbumReview
from sqlalchemy.orm import Session
from scraping.review import Review

def save_reviews_to_db(db: Session, reviews: list[Review]):
    inserted_count = 0
    for review in reviews:
        # Verifica si el álbum ya existe por título
        exists = db.query(AlbumReview).filter_by(title=review.title).first()
        if not exists:
            # Crear una instancia de AlbumReview para añadir a la base de datos
            album_review = AlbumReview(
                title=review.title,
                artist=review.artist,
                release_year=review.release_year,
                rating=review.rating,
                genre=review.genre,
                label=review.label,
                reviewer=review.reviewer,
                review_text=review.review_text,
                url=review.url
            )
            db.add(album_review)
            inserted_count += 1

    db.commit()
    print(f"{inserted_count} reseñas insertadas.")
