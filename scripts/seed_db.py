#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

"""
CLI Script to manually seed or reset the FoodSafe-DX-OS database.
Usage:
    python scripts/seed_db.py [--force]
"""

import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.database import SessionLocal, engine, Base
from app.seed import seed_initial_data


def main():
    force = "--force" in sys.argv
    print(f"Connecting to database and running seed (force={force})...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        result = seed_initial_data(db, force=force)
        print("Seed result:", result)
    finally:
        db.close()


if __name__ == "__main__":
    main()
