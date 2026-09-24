# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal, get_db, wait_for_db
from . import models
from .seed import seed_initial_data
from .routers import facilities, suppliers, batches, inspections_step1, inspections_step2, sample_lockers, incidents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("foodsafe.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager to bootstrap database tables and seed data on boot."""
    logger.info("Initializing FoodSafe-DX-OS database connection...")
    db_ready = wait_for_db(max_retries=10, delay=2)
    if db_ready:
        logger.info("Creating database tables if not exist...")
        Base.metadata.create_all(bind=engine)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Database initialized with {len(tables)} tables: {tables}")

        # Automatically seed realistic initial data if database is empty
        db = SessionLocal()
        try:
            seed_result = seed_initial_data(db, force=False)
            logger.info(f"Seed initialization: {seed_result}")
        except Exception as e:
            logger.error(f"Error during automatic database seeding: {e}")
        finally:
            db.close()
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

# Register API Routers
app.include_router(facilities.router)
app.include_router(suppliers.router)
app.include_router(batches.router)
app.include_router(inspections_step1.router)
app.include_router(inspections_step2.router)
app.include_router(sample_lockers.router)
app.include_router(incidents.router)


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


@app.get("/db/stats", tags=["Database"])
def get_database_statistics(db: Session = Depends(get_db)):
    """Return entity count statistics in the database."""
    return {
        "facilities": db.query(models.Facility).count(),
        "suppliers": db.query(models.Supplier).count(),
        "ingredient_batches": db.query(models.IngredientBatch).count(),
        "inspections_step1": db.query(models.InspectionStep1).count(),
        "inspections_step2": db.query(models.InspectionStep2).count(),
        "sample_lockers": db.query(models.SampleLocker).count(),
        "incident_reports": db.query(models.IncidentReport).count(),
    }


@app.post("/db/seed", tags=["Database"])
def trigger_database_seed(force: bool = Query(False, description="Xóa và nạp lại từ đầu"), db: Session = Depends(get_db)):
    """API endpoint to trigger or reset realistic seed data for live demo."""
    try:
        result = seed_initial_data(db, force=force)
        stats = {
            "facilities": db.query(models.Facility).count(),
            "suppliers": db.query(models.Supplier).count(),
            "ingredient_batches": db.query(models.IngredientBatch).count(),
            "inspections_step1": db.query(models.InspectionStep1).count(),
            "inspections_step2": db.query(models.InspectionStep2).count(),
            "sample_lockers": db.query(models.SampleLocker).count(),
            "incident_reports": db.query(models.IncidentReport).count(),
        }
        return {
            "action": "seed",
            "result": result,
            "current_stats": stats,
        }
    except Exception as e:
        logger.error(f"Seeding failed: {e}")
        return {
            "status": "error",
            "message": str(e),
        }
