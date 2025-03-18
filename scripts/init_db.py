# Description: Script para crear las tablas en la base de datos. Ejecutar este script antes de ejecutar el script main_scraper.py siempre que se añada/modifique algún modelo.

import sys
import os
# Agregar la ruta de la raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import engine, Base
from database.models import AlbumReview 

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")

if __name__ == "__main__":
    create_tables()
