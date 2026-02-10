from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.graph import Graph
from ..core.storage import StorageManager
from ..core.code_generator import CodeGenerator, ValidationError
from .dependencies import get_storage

router = APIRouter(prefix="/api/graphs", tags=["graphs"])


@router.post("", response_model=Graph)
async def create_graph(graph: Graph, storage: StorageManager = Depends(get_storage)):
    """Create a new graph"""
    try:
        storage.save_graph(graph)
        return graph
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[dict])
async def list_graphs(storage: StorageManager = Depends(get_storage)):
    """List all saved graphs"""
    try:
        return storage.list_graphs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{graph_id}", response_model=Graph)
async def get_graph(graph_id: str, storage: StorageManager = Depends(get_storage)):
    """Get a graph by ID"""
    try:
        graph = storage.load_graph(graph_id)
        if graph is None:
            raise HTTPException(status_code=404, detail="Graph not found")

        return graph
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{graph_id}", response_model=Graph)
async def update_graph(graph_id: str, graph: Graph, storage: StorageManager = Depends(get_storage)):
    """Update an existing graph"""
    try:
        # Ensure ID matches
        if graph.id != graph_id:
            raise HTTPException(status_code=400, detail="Graph ID mismatch")

        storage.save_graph(graph)
        return graph
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{graph_id}")
async def delete_graph(graph_id: str, storage: StorageManager = Depends(get_storage)):
    """Delete a graph"""
    try:
        success = storage.delete_graph(graph_id)
        if not success:
            raise HTTPException(status_code=404, detail="Graph not found")
        return {"success": True}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{graph_id}/validate")
async def validate_graph(graph_id: str, storage: StorageManager = Depends(get_storage)):
    """Validate a graph"""
    try:
        graph = storage.load_graph(graph_id)
        if graph is None:
            raise HTTPException(status_code=404, detail="Graph not found")

        generator = CodeGenerator(graph)
        code = generator.generate()

        return {
            "valid": True,
            "code": code
        }
    except ValidationError as e:
        return {
            "valid": False,
            "error": str(e)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate", response_model=dict)
async def validate_graph_inline(graph: Graph):
    """Validate a graph without saving it"""
    try:
        generator = CodeGenerator(graph)
        code = generator.generate()

        return {
            "valid": True,
            "code": code
        }
    except ValidationError as e:
        return {
            "valid": False,
            "error": str(e)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
