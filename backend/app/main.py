from fastapi import FastAPI

from app.api import auth, links
from app.core.database import engine, Base

app = FastAPI(title="URL Shortener API", version="1.0")

# Создаем таблицы, если они еще не созданы
Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(links.router, prefix="/api/links", tags=["links"])