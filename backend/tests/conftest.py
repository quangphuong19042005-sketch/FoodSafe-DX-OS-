# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.seed import seed_initial_data


@pytest.fixture(scope="session")
def client():
    """FastAPI TestClient fixture."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def db():
    """SQLAlchemy database session fixture with preloaded seed data."""
    session = SessionLocal()
    try:
        seed_initial_data(session, force=False)
        yield session
    finally:
        session.close()
