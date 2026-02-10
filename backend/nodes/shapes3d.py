from pydantic import Field
from typing import Dict
from .base import NodeBase


class SphereNode(NodeBase):
    """3D Sphere"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    radius: str = Field(default="1.0")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="1.0", description="Face opacity")
    stroke_opacity: str = Field(default="1.0", description="Edge opacity")
    resolution: str = Field(default="(20, 20)", description="UV resolution")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Sphere(radius={{param_radius}}, color={{param_color}}, fill_opacity={self.fill_opacity}, stroke_opacity={self.stroke_opacity}, resolution={self.resolution})'
        code += f'.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_radius": "Number",
            "param_position": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 3D"


class CubeNode(NodeBase):
    """3D Cube"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    side_length: str = Field(default="2.0")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="1.0", description="Face opacity")
    stroke_opacity: str = Field(default="1.0", description="Edge opacity")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Cube(side_length={{param_side_length}}, color={{param_color}}, fill_opacity={self.fill_opacity}, stroke_opacity={self.stroke_opacity})'
        code += f'.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_side_length": "Number",
            "param_position": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 3D"


class ConeNode(NodeBase):
    """3D Cone"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    base_radius: str = Field(default="1.0")
    height: str = Field(default="2.0")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="1.0", description="Face opacity")
    stroke_opacity: str = Field(default="1.0", description="Edge opacity")
    resolution: str = Field(default="20")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Cone(base_radius={self.base_radius}, height={{param_height}}, color={{param_color}}, fill_opacity={self.fill_opacity}, stroke_opacity={self.stroke_opacity}, resolution={self.resolution})'
        code += f'.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_height": "Number",
            "param_position": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 3D"


class CylinderNode(NodeBase):
    """3D Cylinder"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    radius: str = Field(default="1.0")
    height: str = Field(default="2.0")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="1.0", description="Face opacity")
    stroke_opacity: str = Field(default="1.0", description="Edge opacity")
    resolution: str = Field(default="20")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Cylinder(radius={{param_radius}}, height={{param_height}}, color={{param_color}}, fill_opacity={self.fill_opacity}, stroke_opacity={self.stroke_opacity}, resolution={self.resolution})'
        code += f'.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_radius": "Number",
            "param_height": "Number",
            "param_position": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 3D"


class TorusNode(NodeBase):
    """3D Torus"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    major_radius: str = Field(default="1.5")
    minor_radius: str = Field(default="0.5")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="1.0", description="Face opacity")
    stroke_opacity: str = Field(default="1.0", description="Edge opacity")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Torus(major_radius={{param_major_radius}}, minor_radius={{param_minor_radius}}, color={{param_color}}, fill_opacity={self.fill_opacity}, stroke_opacity={self.stroke_opacity})'
        code += f'.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_major_radius": "Number",
            "param_minor_radius": "Number",
            "param_position": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 3D"


class Axes3DNode(NodeBase):
    """3D Coordinate System"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    x_range: str = Field(default="[-5, 5, 1]", description="[min, max, step]")
    y_range: str = Field(default="[-5, 5, 1]", description="[min, max, step]")
    z_range: str = Field(default="[-5, 5, 1]", description="[min, max, step]")
    x_length: str = Field(default="10.0")
    y_length: str = Field(default="10.0")
    z_length: str = Field(default="6.0")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        code = f'''{var_name} = ThreeDAxes(
            x_range={self.x_range},
            y_range={self.y_range},
            z_range={self.z_range},
            x_length={self.x_length},
            y_length={self.y_length},
            z_length={self.z_length}
        )'''
        code += f'.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_position": "Vec3"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"axes": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 3D"
