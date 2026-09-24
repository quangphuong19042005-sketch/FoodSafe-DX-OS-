# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from .database import engine, Base, get_db, wait_for_db
from . import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("foodsafe.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager to bootstrap database tables on boot."""
    logger.info("Initializing FoodSafe-DX-OS database connection...")
    db_ready = wait_for_db(max_retries=10, delay=2)
    if db_ready:
        logger.info("Creating database tables if not exist...")
        Base.metadata.create_all(bind=engine)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Database initialized with {len(tables)} tables: {tables}")
    else:
        logger.warning("Database unavailable during lifespan startup.")
    yield
    logger.info("Shutting down FoodSafe-DX-OS Backend.")


app = FastAPI(
    title="FoodSafe-DX-OS Backend API",
    description="Hệ điều hành Doanh nghiệp số An toàn Thực phẩm - Bếp ăn Bán trú & Doanh nghiệp",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Setup
cors_origins_env = os.getenv("CORS_ORIGINS", "*")
origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
def root():
    """Root entrypoint returning system metadata."""
    return {
        "system": "FoodSafe-DX-OS",
        "version": "1.0.0",
        "status": "OPERATIONAL",
        "spaces": {
            "human": "Kitchen & Audit Portal",
            "process": "3-Step Inspection & Poka-yoke Engine",
            "data": "PostgreSQL SSOT & Real-time BI",
            "intelligence": "Agentic Graph Tracer & Microbiology RAG",
        },
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Healthcheck endpoint for Docker container probes."""
    return {
        "status": "healthy",
        "database": "connected" if os.getenv("DATABASE_URL") else "unconfigured",
    }


@app.get("/db/tables", tags=["Database"])
def list_database_tables():
    """Check list of tables registered in the PostgreSQL database."""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return {
            "status": "success",
            "table_count": len(tables),
            "tables": tables,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }
