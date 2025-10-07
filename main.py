"""Top-level runner that prefers the package `backend` when available.

This file keeps backward compatibility for people who expect to run
``python main.py`` from the repo root. When the `backend` package exists we
reuse its FastAPI app object; otherwise we fall back to a minimal app defined
here (same routes as older layout).
"""
import importlib
import logging
from typing import Optional

logger = logging.getLogger("repo.root")


def _load_app() -> Optional[object]:
    try:
        backend = importlib.import_module("backend.main")
        app = getattr(backend, "app")
        logger.info("Using backend.main:app as FastAPI application")
        return app
    except Exception:
        logger.debug("backend.main not importable; falling back to local app")

    try:
        # Older layout: routes live at top-level `routes` package
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from routes import simulation, ai_engine

        logging.basicConfig(level=logging.INFO)
        logger_local = logging.getLogger("relay_backend")

        app = FastAPI(title="Relay Attack Backend", version="0.1")

        origins = [
            "http://localhost:5173",
            "http://localhost:3000",
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app.include_router(simulation.router, prefix="/simulate", tags=["simulate"])
        app.include_router(ai_engine.router, prefix="/ai", tags=["ai"])


        @app.get("/")
        async def root():
            return {"status": "Backend Active", "version": "0.1"}

        return app
    except Exception:
        logger.exception("Failed to create a fallback FastAPI app")
        return None


app = _load_app()


if __name__ == "__main__":
    import uvicorn

    if app is None:
        logger.error("No FastAPI app available to run. Exiting.")
    else:
        logger.info("Starting FastAPI app on http://127.0.0.1:8000")
        # Pass the app object directly. Reload is enabled for developer convenience.
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
