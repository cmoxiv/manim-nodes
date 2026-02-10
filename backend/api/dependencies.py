"""FastAPI dependency injection"""
from fastapi import Request
from ..core.storage import StorageManager
from ..core.renderer import Renderer, ExportQueue


def get_storage(request: Request) -> StorageManager:
    """Get the StorageManager instance from app state"""
    return request.app.state.storage


def get_renderer(request: Request) -> Renderer:
    """Get the Renderer instance from app state"""
    return request.app.state.renderer


def get_export_queue(request: Request) -> ExportQueue:
    """Get the ExportQueue instance from app state"""
    return request.app.state.export_queue
