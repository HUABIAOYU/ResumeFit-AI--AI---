import logging
import os
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import init_db
from api.auth import router as auth_router
from api.resumes import router as resumes_router
from api.analyses import router as analyses_router


def setup_logging():
    os.makedirs(settings.log_dir, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        filename=os.path.join(settings.log_dir, "app.log"),
        maxBytes=settings.log_max_bytes,
        backupCount=settings.log_backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 统一配置所有 logger
    for logger_name in (None, "uvicorn", "uvicorn.access", "uvicorn.error"):
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
        logger.handlers.clear()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await init_db()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(resumes_router)
app.include_router(analyses_router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
