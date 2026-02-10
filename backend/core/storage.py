import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from ..models.graph import Graph


class StorageManager:
    """Manages file storage for graphs and generated files"""

    def __init__(self, base_dir: str = None):
        """
        Initialize storage manager.

        Args:
            base_dir: Base directory for storage (default: ~/manim-nodes)
        """
        if base_dir is None:
            base_dir = os.path.expanduser("~/manim-nodes")

        self.base_dir = Path(base_dir)
        self.projects_dir = self.base_dir / "projects"
        self.exports_dir = self.base_dir / "exports"
        self.temp_dir = self.base_dir / "temp"

        # Create directories if they don't exist
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def save_graph(self, graph: Graph) -> str:
        """
        Save graph to disk.

        Args:
            graph: Graph object to save

        Returns:
            Path to saved file
        """
        self._validate_path(graph.id)

        file_path = self.projects_dir / f"{graph.id}.json"

        with open(file_path, "w") as f:
            json.dump(graph.model_dump(), f, indent=2)

        return str(file_path)

    def load_graph(self, graph_id: str) -> Optional[Graph]:
        """
        Load graph from disk.

        Args:
            graph_id: ID of graph to load

        Returns:
            Graph object or None if not found
        """
        self._validate_path(graph_id)

        file_path = self.projects_dir / f"{graph_id}.json"

        if not file_path.exists():
            return None

        with open(file_path, "r") as f:
            data = json.load(f)

        return Graph(**data)

    def delete_graph(self, graph_id: str) -> bool:
        """
        Delete graph from disk.

        Args:
            graph_id: ID of graph to delete

        Returns:
            True if deleted, False if not found
        """
        self._validate_path(graph_id)

        file_path = self.projects_dir / f"{graph_id}.json"

        if file_path.exists():
            file_path.unlink()
            return True

        return False

    def list_graphs(self) -> list[dict]:
        """
        List all saved graphs.

        Returns:
            List of graph metadata (id, name, modified_time)
        """
        graphs = []

        for file_path in self.projects_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    graphs.append({
                        "id": data.get("id"),
                        "name": data.get("name"),
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
            except Exception:
                # Skip invalid files
                continue

        return sorted(graphs, key=lambda x: x["modified"], reverse=True)

    def get_temp_path(self, filename: str) -> Path:
        """Get path for temporary file"""
        self._validate_path(filename)
        return self.temp_dir / filename

    def get_export_path(self, filename: str) -> Path:
        """Get path for export file"""
        self._validate_path(filename)
        return self.exports_dir / filename

    def cleanup_old_temp_files(self, hours: int = 1):
        """
        Delete temporary files older than specified hours.

        Args:
            hours: Age threshold in hours
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)

        for file_path in self.temp_dir.iterdir():
            if file_path.is_file():
                modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if modified_time < cutoff_time:
                    try:
                        file_path.unlink()
                    except Exception:
                        pass  # Ignore errors during cleanup

    def _validate_path(self, path_component: str):
        """
        Validate path component to prevent directory traversal attacks.

        Args:
            path_component: Path component to validate

        Raises:
            ValueError if path is invalid
        """
        # Check for path traversal attempts
        if ".." in path_component or "/" in path_component or "\\" in path_component:
            raise ValueError("Invalid path component")

        # Check for null bytes
        if "\x00" in path_component:
            raise ValueError("Invalid path component")
