# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FoodSafe-DX-OS Backend API",
    description="Hệ điều hành Doanh nghiệp số An toàn Thực phẩm - Bếp ăn Bán trú & Doanh nghiệp",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware setup
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
