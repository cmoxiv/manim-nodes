from pydantic import BaseModel, Field
from typing import Dict, Any


class NodeData(BaseModel):
    """Represents a single node in the graph"""
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, Any]
    parentNode: str | None = None
    extent: str | None = None
    style: Dict[str, Any] | None = None
    zIndex: int | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "node-1",
                "type": "Circle",
                "position": {"x": 100, "y": 100},
                "data": {
                    "radius": 1.0,
                    "color": "#FFFFFF",
                    "fill_opacity": 0.0
                }
            }
        }
