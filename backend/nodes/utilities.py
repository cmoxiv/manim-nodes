from pydantic import Field
from typing import Dict
from .base import NodeBase


class GroupNode(NodeBase):
    """Group multiple shapes together"""
    pivot: str = Field(
        default="center",
        description="Pivot point for the group"
    )

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = VGroup()'

    def get_inputs(self) -> Dict[str, str]:
        return {
            "obj1": "Mobject",
            "obj2": "Mobject",
            "obj3": "Mobject",
            "obj4": "Mobject",
            "obj5": "Mobject",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "2D"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        if "properties" in schema and "pivot" in schema["properties"]:
            schema["properties"]["pivot"]["enum"] = [
                "center", "first", "last", "mean", "min", "max"
            ]
        return schema


class TextCharacterNode(NodeBase):
    """Select specific character(s) from a Text/MathTex object by index or letter"""
    mode: str = Field(default="index", description="Selection mode: index or letter")
    index: str = Field(default="0", description="Character index (used in index mode)")
    letter: str = Field(default="", description="Letter to match (used in letter mode)")

    def to_manim_code(self, var_name: str) -> str:
        if self.mode == "letter":
            return f'{var_name} = VGroup(*[{{input_mobject}}[i] for i, c in enumerate({{input_mobject}}.text) if c == "{self.letter}"])'
        return f'{var_name} = {{input_mobject}}[{self.index}]'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"character": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Text & Math"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        if "properties" in schema and "mode" in schema["properties"]:
            schema["properties"]["mode"]["enum"] = ["index", "letter"]
        return schema


class TransformNode(NodeBase):
    """Apply a 2D transformation matrix (augmented 3x3 homogeneous coordinates)"""
    animate: bool = Field(default=True, description="Animate (True) or apply instantly (False)")
    m11: str = Field(default="1", description="Scale/rotate X (a)")
    m12: str = Field(default="0", description="Skew X (b)")
    m13: str = Field(default="0", description="Translate X (tx)")
    m21: str = Field(default="0", description="Skew Y (c)")
    m22: str = Field(default="1", description="Scale/rotate Y (d)")
    m23: str = Field(default="0", description="Translate Y (ty)")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name}_target = {{input_mobject}}.copy(); {var_name}_target.apply_matrix({{MATRIX_2X2}}); {var_name}_target.shift({{TRANSLATION}}); {var_name} = Transform({{input_mobject}}, {var_name}_target, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {
            "mobject": "Mobject",
            "matrix": "Matrix"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "mobject_out": "Mobject"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        schema["matrixGrid"] = {
            "rows": 2,
            "cols": 3,
            "fields": ["m11", "m12", "m13", "m21", "m22", "m23"],
            "note": "Bottom row [0, 0, 1] is fixed for 2D transforms"
        }
        return schema
