# server/main.py
from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import List

from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, Response
from starlette.middleware.gzip import GZipMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict


# -----------------------------
# Настройки приложения (через env)
# -----------------------------
class Settings(BaseSettings):
    APP_NAME: str = "KEIS CRM PRO AI – API"
    APP_VERSION: str = "0.1.0"

    # Где искать собранный фронт (папка dist)
    FRONT_DIST: Path = Path(__file__).resolve().parent / "dist"

    # Префикс API (оставляем /api для фронтового прокси/alias)
    API_PREFIX: str = "/api"

    # CORS: список доменов через запятую или звёздочка
    CORS_ALLOW_ORIGINS: str = "http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174"
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Включить SPA fallback
    SPA_FALLBACK: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> List[str]:
        raw = (self.CORS_ALLOW_ORIGINS or "").strip()
        if raw == "*" or raw == "":
            return ["*"]
        return [x.strip() for x in raw.split(",") if x.strip()]


settings = Settings()


# -----------------------------
# Логирование
# -----------------------------
logger = logging.getLogger("keis.api")
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s [%(name)s] %(message)s",
)


# -----------------------------
# Инициализация FastAPI
# -----------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",  # открытая схема — под префиксом API
)

# Сжатие ответов
app.add_middleware(GZipMiddleware, minimum_size=1024)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# -----------------------------
# Runtime env.js endpoint
# -----------------------------

@app.get("/env.js", include_in_schema=False)
def env_js():
    api = os.getenv("PUBLIC_API_BASE", "/api")
    return Response(
        media_type="application/javascript",
        content=f'window.__ENV__={{API_BASE:"{api}"}};'
    )

# -----------------------------
# API v1 роутер (плейсхолдеры)
# -----------------------------
api_v1 = APIRouter(prefix=f"{settings.API_PREFIX}/v1", tags=["v1"])


@api_v1.get("/health", summary="Проверка состояния API")
async def api_health():
    return {"status": "ok", "service": settings.APP_NAME, "version": settings.APP_VERSION}


@api_v1.get("/version", summary="Версия сервиса")
async def api_version():
    return {"version": settings.APP_VERSION}


# Пример плейсхолдеров для будущих модулей
@api_v1.get("/deals", summary="Список сделок (плейсхолдер)")
async def list_deals():
    # позже подключим реальную БД/сервисы
    return {"items": [], "total": 0}


@api_v1.get("/users", summary="Список пользователей (плейсхолдер)")
async def list_users():
    return {"items": [], "total": 0}


app.include_router(api_v1)


# -----------------------------
# Health на корне (для внешних балансировщиков)
# -----------------------------
@app.get("/health", tags=["meta"])
async def health_root():
    return {"status": "ok"}


@app.get("/version", tags=["meta"])
async def version_root():
    return {"version": settings.APP_VERSION}


# -----------------------------
# Статика и SPA (React/Vite)
# -----------------------------
# Путь до dist:
DIST_DIR: Path = Path(settings.FRONT_DIST).resolve()
INDEX_HTML: Path = DIST_DIR / "index.html"
ASSETS_DIR: Path = DIST_DIR / "assets"

if DIST_DIR.exists() and INDEX_HTML.exists():
    # /assets — отдаем как статические файлы
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

    # Главная — отдаем index.html
    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(str(INDEX_HTML))

    # SPA fallback: любой маршрут НЕ начинающийся с /api или /assets — отдаем index.html
    if settings.SPA_FALLBACK:
        @app.get("/{full_path:path}", include_in_schema=False)
        async def spa_fallback(full_path: str, request: Request):
            # Не перехватываем api и assets
            path = "/" + full_path.lstrip("/")
            if path.startswith(settings.API_PREFIX) or path.startswith("/assets"):
                return JSONResponse({"detail": "Not found"}, status_code=404)
            # Если фронт собран — отдаем index.html
            if INDEX_HTML.exists():
                return FileResponse(str(INDEX_HTML))
            return PlainTextResponse("Frontend bundle not found. Build the app (`npm run build`).", status_code=500)

    logger.info("Static SPA mounted from: %s", str(DIST_DIR))
else:
    logger.warning("FRONT_DIST не найден или пуст: %s", str(DIST_DIR))
    logger.warning("Собери фронтенд: `npm run build` — тогда сервер будет отдавать SPA.")


# -----------------------------
# Точка входа (локальный запуск)
# -----------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "8000")),
        reload=True,
        reload_dirs=[str(Path(__file__).parent)],
        log_level="info",
    )