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


class _ConstVecNode(NodeBase):
    """Base for constant vector nodes (Manim built-ins). No code generated."""

    # Subclasses set these
    _const_name: str = ""
    _values: str = ""

    def to_manim_code(self, var_name: str) -> str:
        return ""  # No code needed — references Manim built-in constant

    def get_inputs(self) -> Dict[str, str]:
        return {}

    def get_outputs(self) -> Dict[str, str]:
        return {"vector": "Vec3"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class RightNode(_ConstVecNode):
    """RIGHT → [1, 0, 0]"""
    _const_name: str = "RIGHT"
    _values: str = "1, 0, 0"

class LeftNode(_ConstVecNode):
    """LEFT → [-1, 0, 0]"""
    _const_name: str = "LEFT"
    _values: str = "-1, 0, 0"

class UpNode(_ConstVecNode):
    """UP → [0, 1, 0]"""
    _const_name: str = "UP"
    _values: str = "0, 1, 0"

class DownNode(_ConstVecNode):
    """DOWN → [0, -1, 0]"""
    _const_name: str = "DOWN"
    _values: str = "0, -1, 0"

class OutNode(_ConstVecNode):
    """OUT → [0, 0, 1]"""
    _const_name: str = "OUT"
    _values: str = "0, 0, 1"

class InNode(_ConstVecNode):
    """IN → [0, 0, -1]"""
    _const_name: str = "IN"
    _values: str = "0, 0, -1"

class OriginNode(_ConstVecNode):
    """ORIGIN → [0, 0, 0]"""
    _const_name: str = "ORIGIN"
    _values: str = "0, 0, 0"

class XNode(_ConstVecNode):
    """X → [1, 0, 0] (same as RIGHT)"""
    _const_name: str = "RIGHT"
    _values: str = "1, 0, 0"

class YNode(_ConstVecNode):
    """Y → [0, 1, 0] (same as UP)"""
    _const_name: str = "UP"
    _values: str = "0, 1, 0"

class ZNode(_ConstVecNode):
    """Z → [0, 0, 1] (same as OUT)"""
    _const_name: str = "OUT"
    _values: str = "0, 0, 1"


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


class NegateNode(NodeBase):
    """Negate a number"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = -({{input_a}})'

    def get_inputs(self) -> Dict[str, str]:
        return {"a": "Number"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Number"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


# ── Vector operations ──

class Vec3AddNode(NodeBase):
    """Add two vectors"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = (np.array({{input_a}}) + np.array({{input_b}})).tolist()'

    def get_inputs(self) -> Dict[str, str]:
        return {"a": "Vec3", "b": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Vec3"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class Vec3SubtractNode(NodeBase):
    """Subtract two vectors"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = (np.array({{input_a}}) - np.array({{input_b}})).tolist()'

    def get_inputs(self) -> Dict[str, str]:
        return {"a": "Vec3", "b": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Vec3"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class Vec3ScaleNode(NodeBase):
    """Multiply a vector by a scalar"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = (np.array({{input_vector}}) * {{input_scalar}}).tolist()'

    def get_inputs(self) -> Dict[str, str]:
        return {"vector": "Vec3", "scalar": "Number"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Vec3"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class Vec3NegateNode(NodeBase):
    """Negate a vector"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = (-np.array({{input_vector}})).tolist()'

    def get_inputs(self) -> Dict[str, str]:
        return {"vector": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Vec3"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class Vec3DotNode(NodeBase):
    """Dot product of two vectors"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = float(np.dot({{input_a}}, {{input_b}}))'

    def get_inputs(self) -> Dict[str, str]:
        return {"a": "Vec3", "b": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Number"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class Vec3CrossNode(NodeBase):
    """Cross product of two vectors"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = np.cross({{input_a}}, {{input_b}}).tolist()'

    def get_inputs(self) -> Dict[str, str]:
        return {"a": "Vec3", "b": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Vec3"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class Vec3LengthNode(NodeBase):
    """Length (magnitude) of a vector"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = float(np.linalg.norm({{input_vector}}))'

    def get_inputs(self) -> Dict[str, str]:
        return {"vector": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Number"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class Vec3NormalizeNode(NodeBase):
    """Normalize a vector to unit length"""

    def to_manim_code(self, var_name: str) -> str:
        return f'_v = np.array({{input_vector}}); {var_name} = (_v / (np.linalg.norm(_v) + 1e-10)).tolist()'

    def get_inputs(self) -> Dict[str, str]:
        return {"vector": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Vec3"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


# ── Matrix operations ──

class MatrixAddNode(NodeBase):
    """Add two matrices"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = np.add({{input_a}}, {{input_b}})'

    def get_inputs(self) -> Dict[str, str]:
        return {"a": "Matrix", "b": "Matrix"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Matrix"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class MatrixSubtractNode(NodeBase):
    """Subtract two matrices"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = np.subtract({{input_a}}, {{input_b}})'

    def get_inputs(self) -> Dict[str, str]:
        return {"a": "Matrix", "b": "Matrix"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Matrix"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class MatrixInverseNode(NodeBase):
    """Inverse of a matrix"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = np.linalg.inv({{input_matrix}})'

    def get_inputs(self) -> Dict[str, str]:
        return {"matrix": "Matrix"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Matrix"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class MatrixTransposeNode(NodeBase):
    """Transpose of a matrix"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = np.transpose({{input_matrix}})'

    def get_inputs(self) -> Dict[str, str]:
        return {"matrix": "Matrix"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Matrix"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class MatrixNegateNode(NodeBase):
    """Negate a matrix"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = -{{input_matrix}}'

    def get_inputs(self) -> Dict[str, str]:
        return {"matrix": "Matrix"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Matrix"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class MatrixDeterminantNode(NodeBase):
    """Determinant of a matrix"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = float(np.linalg.det({{input_matrix}}))'

    def get_inputs(self) -> Dict[str, str]:
        return {"matrix": "Matrix"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Number"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class MatrixVecMultiplyNode(NodeBase):
    """Multiply a matrix by a vector"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = np.matmul({{input_matrix}}, {{input_vector}}).tolist()'

    def get_inputs(self) -> Dict[str, str]:
        return {"matrix": "Matrix", "vector": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {"result": "Vec3"}

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


class TranslateMatrixNode(NodeBase):
    """Build a 4x4 translation matrix"""
    translation: str = Field(default="[0, 0, 0]", description="Translation [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        return (
            f'_t = {{param_translation}}\n'
            f'        {var_name} = np.array('
            f'[[1, 0, 0, _t[0]], [0, 1, 0, _t[1]], [0, 0, 1, _t[2]], [0, 0, 0, 1]]'
            f', dtype=float)'
        )

    def get_inputs(self) -> Dict[str, str]:
        return {"param_translation": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {"matrix": "Matrix"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class RotateMatrixNode(NodeBase):
    """Build a 4x4 rotation matrix (axis-angle via Rodrigues' formula)"""
    angle: str = Field(default="0", description="Angle in degrees")
    axis: str = Field(default="[0, 0, 1]", description="Rotation axis [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        lines = [
            f'_a_{var_name} = np.radians({{param_angle}})',
            f'_ax_{var_name} = np.array({{param_axis}}, dtype=float)',
            f'_ax_{var_name} = _ax_{var_name} / (np.linalg.norm(_ax_{var_name}) + 1e-10)',
            f'_c, _s = np.cos(_a_{var_name}), np.sin(_a_{var_name})',
            f'_x, _y, _z = _ax_{var_name}',
            f'_R = np.array(['
            f'[_c + _x*_x*(1-_c), _x*_y*(1-_c) - _z*_s, _x*_z*(1-_c) + _y*_s],'
            f' [_y*_x*(1-_c) + _z*_s, _c + _y*_y*(1-_c), _y*_z*(1-_c) - _x*_s],'
            f' [_z*_x*(1-_c) - _y*_s, _z*_y*(1-_c) + _x*_s, _c + _z*_z*(1-_c)]])',
            f'{var_name} = np.eye(4)',
            f'{var_name}[:3, :3] = _R',
        ]
        return '\n        '.join(lines)

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_angle": "Number",
            "param_axis": "Vec3",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"matrix": "Matrix"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class ScaleMatrixNode(NodeBase):
    """Build a 4x4 scale matrix"""
    scale: str = Field(default="[1, 1, 1]", description="Scale [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        return (
            f'_s = {{param_scale}}\n'
            f'        {var_name} = np.array('
            f'[[_s[0], 0, 0, 0], [0, _s[1], 0, 0], [0, 0, _s[2], 0], [0, 0, 0, 1]]'
            f', dtype=float)'
        )

    def get_inputs(self) -> Dict[str, str]:
        return {"param_scale": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {"matrix": "Matrix"}

    @classmethod
    def get_category(cls) -> str:
        return "Math Ops"


class ComposeMatrixNode(NodeBase):
    """Compose up to 4 transformation matrices (multiplied left to right)"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = {{input_m1}}'

    def get_inputs(self) -> Dict[str, str]:
        return {
            "m1": "Matrix",
            "m2": "Matrix",
            "m3": "Matrix",
            "m4": "Matrix",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"matrix": "Matrix"}

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
