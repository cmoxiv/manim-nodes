from pydantic import Field
from typing import Dict
from .base import NodeBase


class AddNode(NodeBase):
    """Add two numbers"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = {{input_a}} + {{input_b}}'

    def get_inputs(self) -> Dict[str, str]:
        return {"a": "Number", "b": "Number"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Number"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class SubtractNode(NodeBase):
    """Subtract two numbers"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = {{input_a}} - {{input_b}}'

    def get_inputs(self) -> Dict[str, str]:
        return {"a": "Number", "b": "Number"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Number"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class MultiplyNode(NodeBase):
    """Multiply two numbers"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = {{input_a}} * {{input_b}}'

    def get_inputs(self) -> Dict[str, str]:
        return {"a": "Number", "b": "Number"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Number"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class DivideNode(NodeBase):
    """Divide two numbers"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = {{input_a}} / {{input_b}}'

    def get_inputs(self) -> Dict[str, str]:
        return {"a": "Number", "b": "Number"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Number"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class NumberNode(NodeBase):
    """Constant number value"""
    value: str = Field(default="1.0", description="Number value (expression)")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = {self.value}'

    def get_inputs(self) -> Dict[str, str]:
        return {}

    def get_outputs(self) -> Dict[str, str]:
        return {"value": "Number"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class Vec3Node(NodeBase):
    """3D vector/point for positions and directions"""
    values: str = Field(default="0, 0, 0", description="Comma-separated X, Y, Z values (expressions)")

    def to_manim_code(self, var_name: str) -> str:
        val = self.values.strip()
        if val.startswith('[') or val.startswith('('):
            return f'{var_name} = list({val})'
        return f'{var_name} = [{val}]'

    def get_inputs(self) -> Dict[str, str]:
        return {}

    def get_outputs(self) -> Dict[str, str]:
        return {"vector": "Vec3"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class Vec3SplitNode(NodeBase):
    """Split a Vec3 into three separate Number values (X, Y, Z)"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name}_x, {var_name}_y, {var_name}_z = {{input_vector}}'

    def get_inputs(self) -> Dict[str, str]:
        return {"vector": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {
            "x": "Number",
            "y": "Number",
            "z": "Number"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class Vec3CombineNode(NodeBase):
    """Combine three Number values (X, Y, Z) into a Vec3"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = [{{input_x}}, {{input_y}}, {{input_z}}]'

    def get_inputs(self) -> Dict[str, str]:
        return {
            "x": "Number",
            "y": "Number",
            "z": "Number"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"vector": "Vec3"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class MatrixNode(NodeBase):
    """Create a 4x4 transformation matrix"""
    # 4x4 matrix (identity matrix by default)
    m11: str = Field(default="1", description="[1,1]")
    m12: str = Field(default="0", description="[1,2]")
    m13: str = Field(default="0", description="[1,3]")
    m14: str = Field(default="0", description="[1,4]")
    m21: str = Field(default="0", description="[2,1]")
    m22: str = Field(default="1", description="[2,2]")
    m23: str = Field(default="0", description="[2,3]")
    m24: str = Field(default="0", description="[2,4]")
    m31: str = Field(default="0", description="[3,1]")
    m32: str = Field(default="0", description="[3,2]")
    m33: str = Field(default="1", description="[3,3]")
    m34: str = Field(default="0", description="[3,4]")
    m41: str = Field(default="0", description="[4,1]")
    m42: str = Field(default="0", description="[4,2]")
    m43: str = Field(default="0", description="[4,3]")
    m44: str = Field(default="1", description="[4,4]")

    def to_manim_code(self, var_name: str) -> str:
        row1 = f'[{self.m11}, {self.m12}, {self.m13}, {self.m14}]'
        row2 = f'[{self.m21}, {self.m22}, {self.m23}, {self.m24}]'
        row3 = f'[{self.m31}, {self.m32}, {self.m33}, {self.m34}]'
        row4 = f'[{self.m41}, {self.m42}, {self.m43}, {self.m44}]'
        return f'{var_name} = [{row1}, {row2}, {row3}, {row4}]'

    def get_inputs(self) -> Dict[str, str]:
        return {}

    def get_outputs(self) -> Dict[str, str]:
        return {"matrix": "Matrix"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        schema["matrixGrid"] = {
            "rows": 4,
            "cols": 4,
            "fields": [
                "m11", "m12", "m13", "m14",
                "m21", "m22", "m23", "m24",
                "m31", "m32", "m33", "m34",
                "m41", "m42", "m43", "m44"
            ]
        }
        return schema


class MatrixMultiplyNode(NodeBase):
    """Multiply two 3x3 matrices"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = np.matmul({{input_a}}, {{input_b}})'

    def get_inputs(self) -> Dict[str, str]:
        return {"a": "Matrix", "b": "Matrix"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Matrix"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class MatrixScaleNode(NodeBase):
    """Multiply matrix by a scalar"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = np.multiply({{input_matrix}}, {{input_scalar}})'

    def get_inputs(self) -> Dict[str, str]:
        return {"matrix": "Matrix", "scalar": "Number"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Matrix"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class ColorNode(NodeBase):
    """Color value - hex string or MANIM color constant"""
    color_value: str = Field(default="#FFFFFF", description="Hex color or MANIM constant (e.g. RED, BLUE)")

    def to_manim_code(self, var_name: str) -> str:
        # If it looks like a hex color, quote it; otherwise paste as expression
        if self.color_value.startswith('#'):
            return f'{var_name} = "{self.color_value}"'
        return f'{var_name} = {self.color_value}'

    def get_inputs(self) -> Dict[str, str]:
        return {"param_rgb": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {"color": "Color", "r": "Number", "g": "Number", "b": "Number"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"
