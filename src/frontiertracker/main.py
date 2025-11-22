from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.frontiertracker.db.database import engine, Base
from src.frontiertracker.api.v1.routers import router as v1_router
from src.frontiertracker.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Frontier Tracker Service...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database initialized successfully.")
    yield
    # Shutdown (if needed)
    logger.info("🛑 Shutting down Frontier Tracker Service...")

app = FastAPI(
    title="Frontier Tracker Service",
    version="0.1.0",
    lifespan=lifespan
)

# 注册 API 路由
app.include_router(v1_router)

# 跨域中间件配置（根据需要调整）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

@app.get("/health")
async def health_check():
    logger.debug("Health check endpoint called")
    return {"status": "healthy"}