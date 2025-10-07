"""Database setup using SQLAlchemy.

This module tries to be tolerant of either SQLite (default) or a full
database URL supplied via DATABASE_URL. For SQLite we include the
`check_same_thread` connect arg which is required for the common local
setup. For other engines we omit it.
"""
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./relay.db")


def _create_engine(url: str):
    """Create an SQLAlchemy engine with sensible defaults for SQLite vs others."""
    connect_args = {}
    if url.startswith("sqlite:"):
        connect_args = {"check_same_thread": False}
    # Use future flag for SQLAlchemy 1.4+ style where available
    return create_engine(url, connect_args=connect_args, future=True)


engine = _create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables from models. Import models here to ensure metadata is registered."""
    # Importing here avoids circular imports at package import time
    # Prefer the new `backend` package models. Fall back to top-level `models` for
    # backwards compatibility. The legacy `backen` package has been removed.
    try:
        from backend.models import Base  # type: ignore
    except Exception:
        from models import Base  # type: ignore

    Base.metadata.create_all(bind=engine)
