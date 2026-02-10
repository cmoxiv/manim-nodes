from fastapi import APIRouter
from typing import List, Dict, Any
from ..nodes import NODE_REGISTRY

router = APIRouter(prefix="/api/nodes", tags=["nodes"])


@router.get("", response_model=List[Dict[str, Any]])
async def list_nodes():
    """List all available node types"""
    nodes = []

    for node_type, node_class in NODE_REGISTRY.items():
        # Create a sample instance to get schema
        sample = node_class()

        # Get custom schema if available, otherwise use default
        schema = node_class.get_schema() if hasattr(node_class, 'get_schema') else node_class.model_json_schema()

        nodes.append({
            "type": node_type,
            "displayName": node_class.get_display_name(),
            "category": node_class.get_category(),
            "inputs": sample.get_inputs(),
            "outputs": sample.get_outputs(),
            "schema": schema
        })

    return nodes


@router.get("/{node_type}", response_model=Dict[str, Any])
async def get_node_info(node_type: str):
    """Get information about a specific node type"""
    if node_type not in NODE_REGISTRY:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Node type not found")

    node_class = NODE_REGISTRY[node_type]
    sample = node_class()

    # Get custom schema if available, otherwise use default
    schema = node_class.get_schema() if hasattr(node_class, 'get_schema') else node_class.model_json_schema()

    return {
        "type": node_type,
        "displayName": node_class.get_display_name(),
        "category": node_class.get_category(),
        "inputs": sample.get_inputs(),
        "outputs": sample.get_outputs(),
        "schema": schema
    }
