import pandas as pd

def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    # Elimina duplicados
    df = df.drop_duplicates()
    # Rellenar valores nulos básicos
    df['genre'] = df['genre'].fillna('Unknown')
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df = df.dropna(subset=['score'])  # Eliminamos si no hay score
    return df
