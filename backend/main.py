import os
import subprocess
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from backend.api import graphs, export, websocket, nodes, examples
from backend.core.storage import StorageManager
from backend.core.renderer import Renderer, ExportQueue
from backend.core.logging_config import setup_logging, get_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan (startup and shutdown)"""
    # Startup
    logger = setup_logging(log_level="INFO")
    logger.info("Starting Manim Nodes API")

    storage = StorageManager()
    logger.info("Cleaning up old temp files...")
    storage.cleanup_old_temp_files(hours=1)
    logger.info("Startup complete")

    # Initialize services
    renderer = Renderer(storage)
    export_queue = ExportQueue(storage, renderer)

    # Store services in app state for dependency injection
    app.state.storage = storage
    app.state.renderer = renderer
    app.state.export_queue = export_queue

    yield

    # Shutdown (cleanup if needed)
    logger.info("Shutting down Manim Nodes API")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Manim Nodes API",
    description="Visual programming interface for MANIM animations",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(graphs.router)
app.include_router(export.router)
app.include_router(nodes.router)
app.include_router(websocket.router)
app.include_router(examples.router)

# Mount temp files directory (using a temporary storage instance for directory path)
_temp_storage = StorageManager()
app.mount("/temp", StaticFiles(directory=str(_temp_storage.temp_dir)), name="temp")


@app.get("/")
async def root():
    """Serve frontend index.html if available, otherwise API info"""
    static_dir = Path(__file__).parent / "static"
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "name": "Manim Nodes API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/open-folder/{folder}")
async def open_folder(folder: str):
    """Open a storage folder in the system file manager, or return path"""
    storage = _temp_storage
    folders = {
        "exports": storage.exports_dir,
        "previews": storage.temp_dir / "media",
    }
    path = folders.get(folder)
    if path is None:
        raise HTTPException(status_code=400, detail="Unknown folder")
    path.mkdir(parents=True, exist_ok=True)

    # If HOST_DATA_DIR is set (Docker), map container path to host path
    host_data_dir = os.environ.get("HOST_DATA_DIR")
    if host_data_dir:
        host_path = str(path).replace(str(storage.base_dir), host_data_dir)
        return {"ok": True, "path": host_path, "native": False}

    # Native: open in system file manager
    if sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    elif sys.platform == "win32":
        subprocess.Popen(["explorer", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])
    return {"ok": True, "path": str(path), "native": True}


# Serve frontend static files (must be after all API routes)
_static_dir = Path(__file__).parent / "static"
if _static_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(_static_dir / "assets")), name="static-assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Catch-all: serve index.html for SPA client-side routing"""
        return FileResponse(_static_dir / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
