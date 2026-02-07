# app/core/lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
import redis.asyncio as aioredis
from app.core.config import settings
from app.utils.logger import logger

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        redis = aioredis.from_url(settings.REDIS_URL)
        await redis.ping()
        logger.info("✅ Redis is reachable")
        yield  # App runs
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")
        return


