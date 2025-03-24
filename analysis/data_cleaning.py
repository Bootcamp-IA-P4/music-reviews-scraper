import pandas as pd

def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    # Eliminar duplicados
    df = df.drop_duplicates()

    # Rellenar valores nulos con 'Unknown' donde tenga sentido
    for col in ['artist', 'title', 'genre', 'label', 'reviewer']:
        df[col] = df[col].fillna('Unknown').str.strip()

    # Convertir 'rating' a numérico y eliminar los que no tengan nota
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['rating'])

    # Convertir release_year a entero, si es posible
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce').astype('Int64')

    # Limpiar espacios en 'review_text'
    df['review_text'] = df['review_text'].fillna('').str.strip()

    # Corregir casos donde el género venga en mayúsculas y normalizar
    df['genre'] = df['genre'].str.title()

    return df

