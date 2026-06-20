from fastapi import FastAPI
from database import engine, Base
from routes.version_routes_crud import router

app = FastAPI()
app.include_router(router)
Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {
        "message": "VersionForge API Running"
    }