from pydantic import BaseModel, Field
from typing import List, Dict, Any
from .node import NodeData


class EdgeData(BaseModel):
    """Represents a connection between two nodes"""
    id: str
    source: str
    target: str
    sourceHandle: str | None = None
    targetHandle: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "edge-1",
                "source": "node-1",
                "target": "node-2",
                "sourceHandle": "output",
                "targetHandle": "input"
            }
        }


class Graph(BaseModel):
    """Complete graph structure representing a MANIM animation"""
    id: str = Field(default="")
    name: str
    nodes: List[NodeData] = Field(default=[], max_length=200)
    edges: List[EdgeData] = Field(default=[], max_length=500)
    settings: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "graph-123",
                "name": "My First Animation",
                "nodes": [],
                "edges": [],
                "settings": {
                    "resolution": "1080p",
                    "fps": 30,
                    "background_color": "#000000"
                }
            }
        }
