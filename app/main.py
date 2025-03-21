from fastapi import FastAPI
from app.routes import pitchfork, spotify, recommended

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to my music reviews app!"}

app.include_router(spotify.router)
app.include_router(pitchfork.router)
app.include_router(recommended.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
