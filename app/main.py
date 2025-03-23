from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import pitchfork, spotify, recommended

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # O ["*"] para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to my music reviews app!"}

app.include_router(spotify.router)
app.include_router(pitchfork.router)
app.include_router(recommended.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
