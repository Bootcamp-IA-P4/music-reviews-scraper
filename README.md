## 🎶 Music Reviews Project

### 🔢 Descripción

Este proyecto combina **scraping de las críticas musicales Pitchfork**, integración con la **API de Spotify** y una interfaz frontend **Next.js** para ofrecerte recomendaciones de álbumes personalizadas según tus gustos musicales (en concreto, según los úñtimos 200 álbumes que hayas guardado en tu perfil de Spotify). Todo el backend está construido en **FastAPI** y los datos se almacenan en **PostgreSQL**.

**Funcionalidades:**

- Listado de reviews de Pitchfork paginado y filtrable.
- Login con Spotify para acceder a recomendaciones personalizadas: se hace un match entre tus álbumes guardados en Spotify y reviews de Pitchfork.

---

## 📂 Estructura del proyecto

```bash
music_reviews_project/
├── app/                             # Backend con FastAPI
│   ├── core/                        # Archivos de configuración
│   ├── models/                      # SQLAlchemy Models
│   ├── routes/                      # Endpoints
│   ├── services/                    # Scraping & Conexiones con la base de datos
│   ├── utils/                       # Funciones de utilidad
│   └── main.py
│
├── frontend/                        # Frontend con Next.js
├── analysis/                        # Análisis de datos del scraping
├── data/                            # Datos de scraping guardados en csv
├── scripts/                         # Scripts para iniciar base de datos / scraping
│
├── .env
├── requirements.txt
└── README.md
```

---

## 🌐 Instalación

### 1. Clonar el repositorio

```bash
git clone <url_del_repositorio>
cd music_reviews_project
```

### 2. Backend (FastAPI)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Frontend (Next.js)

```bash
cd frontend
npm install
cd ..
```

### 4. Variables de entorno

Crear un archivo `.env` con tus credenciales de Spotify y configuración de la BBDD.

---

## 🎉 Ejecución rápida (con Makefile)

| Comando          | Qué hace                         |
| ---------------- | -------------------------------- |
| `make run-api`   | Levanta solo el backend FastAPI  |
| `make run-front` | Levanta solo el frontend Next.js |
| `make dev`       | Levanta **ambos** en paralelo    |

### Ejemplo:

```bash
make dev
```

El backend correrá en `http://localhost:8000` y el frontend en `http://localhost:3000`

---

## 📚 Endpoints principales (FastAPI)

- `GET /reviews`: Listado paginado y filtrable de reviews.
- `GET /login`: Inicia sesión en Spotify.
- `GET /callback`: Callback de Spotify.
- `GET /saved_albums`: Una vez iniciada sesión en spotify, la redirección muestra el listado de albums guardados
- `GET /recommended_reviews`: Recomendaciones basadas en Spotify.

---

## 💡 Stack Tecnológico

- **Backend:** FastAPI + SQLAlchemy + PostgreSQL
- **Frontend:** Next.js (React) + TailwindCSS
- **Scraping:** BeautifulSoup + Requests
- **Análisis:** Pandas + Seaborn + matplotlib

---

## 📲 Contacto

Proyecto creado por Andrea Alonso Corbeira -
✉️ aalonsocorbeira@gmail.com

---
