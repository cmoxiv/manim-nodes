from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
    """Root endpoint"""
    return {
        "name": "Manim Nodes API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
