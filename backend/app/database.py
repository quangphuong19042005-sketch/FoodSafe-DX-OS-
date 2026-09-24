# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

import os
import time
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("foodsafe.database")

# Database connection URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://foodsafe:foodsafe_secret@db:5432/foodsafe_db"
)

# Engine setup with pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency generator yielding SQLAlchemy database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def wait_for_db(max_retries=10, delay=2):
    """Wait for database server to be ready before initializing tables."""
    retries = 0
    while retries < max_retries:
        try:
            with engine.connect() as connection:
                logger.info("Successfully connected to PostgreSQL database.")
                return True
        except Exception as e:
            retries += 1
            logger.warning(f"Database not ready yet (attempt {retries}/{max_retries}): {e}")
            time.sleep(delay)
    logger.error("Could not connect to database after multiple retries.")
    return False
