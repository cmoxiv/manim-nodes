from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Dict, Any


class NodeBase(BaseModel, ABC):
    """Base class for all node types in the graph"""

    @abstractmethod
    def to_manim_code(self, var_name: str) -> str:
        """
        Generate MANIM Python code for this node.

        Args:
            var_name: Variable name to assign the result to

        Returns:
            Python code string that creates this MANIM object
        """
        pass

    @abstractmethod
    def get_inputs(self) -> Dict[str, str]:
        """
        Return input port definitions for this node.

        Returns:
            Dictionary mapping port name to type (e.g., {"shape": "Mobject"})
        """
        pass

    @abstractmethod
    def get_outputs(self) -> Dict[str, str]:
        """
        Return output port definitions for this node.

        Returns:
            Dictionary mapping port name to type (e.g., {"shape": "Mobject"})
        """
        pass

    @classmethod
    def get_node_type(cls) -> str:
        """Return the node type identifier"""
        return cls.__name__.replace("Node", "")

    @classmethod
    def get_display_name(cls) -> str:
        """Return the human-readable display name"""
        return cls.get_node_type()

    @classmethod
    def get_category(cls) -> str:
        """Return the category for this node (Shapes, Animations, Math, etc.)"""
        return "Uncategorized"

    class Config:
        arbitrary_types_allowed = True
