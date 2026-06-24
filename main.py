from fastapi import FastAPI
from database import engine, Base
from routes.version_routes_crud import router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {
        "message": "VersionForge API Running"
    }