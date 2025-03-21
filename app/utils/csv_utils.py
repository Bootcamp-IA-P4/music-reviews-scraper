import os
import csv

def save_reviews_to_csv(albums):
    if not os.path.exists('data'):
        os.makedirs('data')

    file_path = 'data/albums.csv'
    write_header = not os.path.exists(file_path)

    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(['Title', 'Artist', 'Release Year', 'Rating', 'Genre', 'Label', 'Reviewer', 'Review Text', 'URL'])

        for album in albums:
            writer.writerow([
                album.title or "Unknown",
                album.artist or "Unknown",
                album.release_year or "Unknown",
                album.rating or "Unknown",
                album.genre or "Unknown",
                album.label or "Unknown",
                album.reviewer or "Unknown",
                album.review_text or "Unknown",
                album.url
            ])
